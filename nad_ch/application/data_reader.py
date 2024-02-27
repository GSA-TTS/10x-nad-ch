from geopandas import GeoDataFrame, read_file
import fiona
from typing import Optional
import yaml
import os


class DataReader(object):
    def __init__(self, config_name: Optional[str] = None) -> None:
        self.config_name = config_name
        self.default_config_path = "nad_ch/application/nad_column_maps/default.yaml"
        self.column_map = self.read_column_map()

    def read_column_map(self) -> dict[any]:
        custom_config_path = (
            f"nad_ch/application/nad_column_maps/{self.config_name}.yaml"
        )
        with open(self.default_config_path, "r") as file:
            default_config = yaml.safe_load(file)
        if not os.path.exists(custom_config_path):
            column_map_config = default_config
        else:
            with open(custom_config_path, "r") as file:
                column_map_config = yaml.safe_load(file)
                column_map_config["data_required_fields"] = default_config.get(
                    "data_required_fields"
                )
        return column_map_config

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
        valid_renames = {}
        for nad_column, fields_to_check in column_map.items():
            orig_matched_name = original_names.get(nad_column.lower())
            if orig_matched_name:
                valid_renames[orig_matched_name] = nad_column
                continue
            for field in fields_to_check:
                orig_matched_name = original_names.get(field.lower())
                if orig_matched_name:
                    valid_renames[orig_matched_name] = nad_column
                    break
        gdf = gdf.rename(columns=valid_renames)
        return gdf[[col for col in valid_renames.values()]]

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
