import os
from typing import Dict, List, Optional, IO
from zipfile import ZipFile
import fiona
from geopandas import GeoDataFrame
import pandas as pd
import shapefile
import tempfile
from nad_ch.application.dtos import (
    DataSubmissionReportFeature,
    DataSubmissionReportOverview,
)
from nad_ch.application.interfaces import Storage
import glob
from pathlib import Path
from nad_ch.core.entities import ColumnMap
from collections import Counter


class DataValidator:
    def __init__(self, valid_mappings: Dict[str, str]):
        self.valid_mappings = valid_mappings
        self.domains = {}
        self.required_fields = ColumnMap.required_fields
        self.load_domain_values()
        self.missing_fields = set()
        self.report_overview: Optional[DataSubmissionReportFeature] = None
        self.report_features: Optional[Dict[str, DataSubmissionReportFeature]] = None

    def load_domain_values(self):
        for type in ("domain", "mapper"):
            self.domains[type] = {}
            path = f"nad_ch/application/validation_files/{type}/*.csv"
            file_paths = glob.glob(path)
            for file_path in file_paths:
                field = "_".join(Path(file_path).stem.split("_")[1:])
                df = pd.read_csv(file_path, sep=",", encoding="utf-8")
                df["Source"] = df["Source"].astype(str)
                df["Destination"] = df["Destination"].astype(str)
                self.domains[type][field] = dict(zip(df.Source, df.Destination))

    @staticmethod
    def get_feature_count(gdf: GeoDataFrame) -> int:
        return len(gdf.columns)

    @staticmethod
    def get_record_count(gdf: GeoDataFrame, invalid_rows: bool = False) -> int:
        if invalid_rows:
            return len(gdf[gdf.isnull().any(axis=1)])
        return len(gdf)

    @staticmethod
    def get_features_flagged(features: Dict[str, DataSubmissionReportFeature]) -> int:
        return len(
            [
                k
                for k, v in features.items()
                if v.null_count + v.invalid_domain_count > 0
            ]
        )

    def get_invalid_record_count(self, gdf: GeoDataFrame) -> int:
        existing_required_fields = list(self.valid_mappings.values())
        filters = [
            f"(gdf['{field}'].isin({self.report_features[field].invalid_domains}))"
            for field in existing_required_fields
            if self.report_features[field].invalid_domains
        ]
        filters.append(f"(gdf[{existing_required_fields}].isna().any(axis=1))")
        return len(gdf[eval("|".join(filters))])

    def initialize_overview_details(
        self, gdf: GeoDataFrame, column_map: Dict[str, str]
    ):
        if not self.report_features and not self.report_overview:
            self.report_overview = DataSubmissionReportOverview(
                feature_count=self.get_feature_count(gdf)
            )
            missing_fields = [
                column for column in self.required_fields if column not in gdf.columns
            ]
            self.report_overview.missing_required_fields = missing_fields
            self.report_features = {
                nad_name: DataSubmissionReportFeature(
                    provided_feature_name=provided_name, nad_feature_name=nad_name
                )
                for provided_name, nad_name in column_map.items()
            }

    def update_feature_details(self, gdf: GeoDataFrame):
        for column in gdf.columns:
            feature_submission = self.report_features.get(column)
            if feature_submission:
                # Update null and populated counts
                populated_count = gdf[column].notna().sum()
                null_count = gdf[column].isna().sum()
                feature_submission.populated_count += populated_count
                feature_submission.null_count += null_count

                # Update invalid domain metrics
                column_domain_dict = self.domains["domain"].get(column)
                column_mapper_dict = self.domains["mapper"].get(column)
                if column_domain_dict and column_mapper_dict:
                    filter = ~(
                        (gdf[column].isin(column_domain_dict.keys()))
                        | (
                            (gdf[column].isin(column_mapper_dict.keys()))
                            | (gdf[column].str.lower().isin(column_mapper_dict.keys()))
                        )
                    )
                elif column_domain_dict:
                    filter = ~(gdf[column].isin(column_domain_dict.keys()))
                elif column_mapper_dict:
                    filter = ~(
                        (gdf[column].isin(column_mapper_dict.keys()))
                        | (gdf[column].str.lower().isin(column_mapper_dict.keys()))
                    )
                else:
                    filter = None
                invalid_domain_count, invalid_domains = 0, []
                if filter is not None:
                    gdf_invalid_domains = gdf[filter & (gdf[column].notna())]
                    invalid_domain_count = gdf_invalid_domains.shape[0]
                    invalid_domains = [
                        domain
                        for domain in list(gdf_invalid_domains[column].unique())
                        if domain not in feature_submission.invalid_domains
                    ]
                    valid_domain_count = (
                        gdf.shape[0] - invalid_domain_count - null_count
                    )
                    feature_submission.invalid_domain_count += invalid_domain_count
                    feature_submission.valid_domain_count += valid_domain_count
                    # Can only store up to 100 invalid domains per nad field
                    remaining_slots = 100 - len(feature_submission.invalid_domains)
                    if invalid_domains and remaining_slots > 0:
                        feature_submission.invalid_domains.extend(
                            invalid_domains[:remaining_slots]
                        )

                # Generate frequency table of fields that are domain specific only
                if column_domain_dict:
                    domain_freq = gdf[column].value_counts().to_dict()
                    if feature_submission.domain_frequency:
                        domain_freq = dict(
                            Counter(feature_submission.domain_frequency)
                            + Counter(domain_freq)
                        )
                    # Check if the number of unique domains in frequency dictionary
                    # is 2x greater than maximum expected unique domains
                    if len(domain_freq.keys()) > 2 * len(column_domain_dict.keys()):
                        feature_submission.high_domain_cardinality = True
                        # Reset domain frequency
                        domain_freq = {}
                    feature_submission.domain_frequency = domain_freq

    def update_overview_details(self, gdf: GeoDataFrame):
        self.report_overview.records_count += self.get_record_count(gdf)
        self.report_overview.records_flagged += self.get_invalid_record_count(gdf)

    def finalize_overview_details(self):
        self.report_overview.features_flagged += self.get_features_flagged(
            self.report_features
        )
        # TODO: Add logic for etl_update_required & data_update_required

    def run(self, gdf_batch: GeoDataFrame):
        self.initialize_overview_details(gdf_batch, self.valid_mappings)
        self.update_feature_details(gdf_batch)
        self.update_overview_details(gdf_batch)


class FileValidator:
    def __init__(self, file: IO[bytes], filename: str) -> None:
        self.file = file
        self.filename = filename

    def validate_file(self) -> bool:
        """Confirm that the file is a valid shapefile or geodatabase."""
        if not self._is_zipped():
            return False

        with ZipFile(self.file) as zip_file:
            file_names = zip_file.namelist()
            if not (
                self._is_valid_shapefile(file_names)
                or self._is_valid_geodatabase(file_names)
            ):
                return False

        return True

    def validate_schema(self, column_map: Dict[str, str]) -> bool:
        """Confirm that the schema is accommodated by the selected mapping."""
        with ZipFile(self.file) as zip_file:
            file_names = zip_file.namelist()
            if self._is_valid_shapefile(file_names):
                return self._validate_shapefile_schema(zip_file, column_map)
            elif self._is_valid_geodatabase(file_names):
                return self._validate_gdb_schema(zip_file, column_map)
            else:
                return False

    def _is_zipped(self) -> bool:
        _, file_extension = os.path.splitext(self.filename)
        if file_extension.lower() != ".zip":
            return False

        return True

    def _is_valid_shapefile(self, file_names: List[str]) -> bool:
        required_extensions = {".shp", ".shx", ".dbf"}
        found_extensions = set(os.path.splitext(name)[1].lower() for name in file_names)
        return required_extensions.issubset(found_extensions)

    def _is_valid_geodatabase(self, file_names: List[str]) -> bool:
        return any(
            (name.endswith(".gdb") or name.endswith(".gdb/")) and "/" in name
            for name in file_names
        )

    def _validate_shapefile_schema(
        self, zip_file: ZipFile, expected_schema: Dict[str, str]
    ) -> bool:
        file_names = zip_file.namelist()

        shp_file = next((name for name in file_names if name.endswith(".shp")), None)
        if not shp_file:
            return False

        temp_dir = tempfile.mkdtemp()
        zip_file.extractall(temp_dir)
        path = os.path.join(temp_dir, shp_file)
        sf = shapefile.Reader(path)

        fields = [field[0] for field in sf.fields]
        filtered_fields = [
            item for item in fields if (item != "DeletionFlag" and item != "index")
        ]
        filtered_expected_fields = [
            value for value in expected_schema.values() if value is not None
        ]

        return all(value in filtered_fields for value in filtered_expected_fields)

    def _validate_gdb_schema(
        self, zip_file: ZipFile, expected_schema: Dict[str, str]
    ) -> bool:
        file_names = zip_file.namelist()
        gdb_dir = next((name for name in file_names if name.endswith(".gdb/")), None)

        if not gdb_dir:
            return False

        temp_dir = tempfile.mkdtemp()
        zip_file.extractall(temp_dir)
        gdb_path = os.path.join(temp_dir, gdb_dir)

        layers = fiona.listlayers(gdb_path)

        for layer_name in layers:
            with fiona.open(gdb_path, layer=layer_name) as layer:
                fields = layer.schema["properties"].keys()
                filtered_expected_fields = [
                    value for value in expected_schema.values() if value is not None
                ]
                all_present = all(value in fields for value in filtered_expected_fields)
                if all_present:
                    return True

        return False
