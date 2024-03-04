from geopandas import GeoDataFrame, read_file
import fiona
from typing import Optional, Dict
import yaml
import os


class DataReader(object):
    def __init__(self, column_map: Dict[str, str]) -> None:
        self.required_fields_path = (
            "nad_ch/application/validation_files/required_fields.yaml"
        )
        self.column_map = self.set_column_map(column_map)
        self.valid_renames = {}

    def set_column_map(self, column_map: Dict[str, str]) -> Dict[str, str]:
        with open(self.required_fields_path, "r") as file:
            required_fields = yaml.safe_load(file)
        column_map["data_required_fields"] = required_fields["data_required_fields"]
        return column_map

    def validate_column_map(self):
        column_map = self.column_map["data_column_mapping"]
        column_map_reverse = {}

        for key, values in column_map.items():
            for value in values:
                value_lcase = value.lower()
                if value_lcase in column_map_reverse:
                    column_map_reverse[value_lcase].append(key)
                else:
                    column_map_reverse[value_lcase] = [key]
        duplicates = {k: v for k, v in column_map_reverse.items() if len(v) > 1}
        if duplicates:
            duplicate_nad_fields = ", ".join(
                [" & ".join(nad_fields) for nad_fields in list(duplicates.values())]
            )
            raise Exception(
                f"Duplicate inputs found for destination fields: {duplicate_nad_fields}"
            )

    def rename_columns(self, gdf: GeoDataFrame) -> GeoDataFrame:
        column_map = self.column_map["data_column_mapping"]
        original_names = {col.lower(): col for col in gdf.columns}
        for nad_column, fields_to_check in column_map.items():
            orig_matched_name = original_names.get(nad_column.lower())
            if orig_matched_name:
                self.valid_renames[orig_matched_name] = nad_column
                continue
            for field in fields_to_check:
                orig_matched_name = original_names.get(field.lower())
                if orig_matched_name:
                    self.valid_renames[orig_matched_name] = nad_column
                    break
        gdf = gdf.rename(columns=self.valid_renames)
        return gdf[[col for col in self.valid_renames.values()]]

    def read_file_in_batches(
        self, path: str, table_name: Optional[str] = None, batch_size: int = 100000
    ) -> GeoDataFrame:
        # TODO: Modify to return a joined table; for cases where 1 or more tables
        # are needed to get all fields from source file.
        layers = fiona.listlayers(path)
        if table_name and table_name not in layers:
            raise Exception(f"Table name {table_name} does not exist")
        i = 0
        while True:
            gdf = read_file(path, rows=slice(i, i + batch_size))
            if gdf.shape[0] == 0:
                break
            gdf = self.rename_columns(gdf)
            yield gdf
            i += batch_size
