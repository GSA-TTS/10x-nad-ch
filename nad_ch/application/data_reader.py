from geopandas import GeoDataFrame, read_file
import fiona
from typing import Optional, Dict, Iterator


class DataReader(object):
    def __init__(self, column_map: Dict[str, str]) -> None:
        self.column_map = column_map
        self.valid_renames = {}
        self.validate_column_map()

    def validate_column_map(self):
        column_map_reverse = {}

        for key, value in self.column_map.items():
            if value:
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
        column_map = self.column_map
        original_names = {col.lower(): col for col in gdf.columns}
        for nad_column, raw_field in column_map.items():
            orig_matched_name = original_names.get(nad_column.lower())
            if orig_matched_name:
                self.valid_renames[orig_matched_name] = nad_column
                continue
            if raw_field:
                orig_matched_name = original_names.get(raw_field.lower())
                if orig_matched_name:
                    self.valid_renames[orig_matched_name] = nad_column
        gdf = gdf.rename(columns=self.valid_renames)
        return gdf[[col for col in self.valid_renames.values()]]

    def read_file_in_batches(
        self, path: str, table_name: Optional[str] = None, batch_size: int = 100000
    ) -> Iterator[GeoDataFrame]:
        # TODO: Modify to return a joined table; for cases where 1 or more tables
        # are needed to get all fields from source file.
        if table_name and table_name not in fiona.listlayers(path):
            raise Exception(f"Table name {table_name} does not exist")
        i = 0
        while True:
            gdf = read_file(path, rows=slice(i, i + batch_size))
            if gdf.shape[0] == 0:
                break
            gdf = self.rename_columns(gdf)
            yield gdf
            i += batch_size
