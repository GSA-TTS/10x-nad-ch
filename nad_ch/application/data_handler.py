import os
from geopandas import GeoDataFrame, read_file
import fiona
from typing import Optional, Dict, Iterator
import shutil
from zipfile import ZipFile


class DataHandler(object):
    def __init__(
        self, column_map: Dict[str, str], mapped_data_dir: Optional[str] = None
    ) -> None:
        self.column_map = column_map
        self.mapped_data_dir = mapped_data_dir
        self.mapped_data_path = (
            os.path.join(
                self.mapped_data_dir,
                self.mapped_data_dir.split("/")[-1] + ".shp",
            )
            if self.mapped_data_dir
            else None
        )
        self.zip_file_path = (
            os.path.join(
                self.mapped_data_dir,
                self.mapped_data_dir.split("/")[-1] + ".zip",
            )
            if self.mapped_data_dir
            else None
        )
        self.valid_renames = {}
        self.__validate_column_map()

    def __validate_column_map(self):
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

    def __rename_columns(self, gdf: GeoDataFrame) -> GeoDataFrame:
        column_map = self.column_map
        column_map["geometry"] = "geometry"
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
                if self.mapped_data_dir:
                    # No more batches to process, create zip file
                    self.__zip_mapped_data()
                break
            gdf = self.__rename_columns(gdf)
            if self.mapped_data_dir:
                self.__write_mapped_batch(gdf, i == 0)
            yield gdf
            i += batch_size

    def __write_mapped_batch(self, gdf: GeoDataFrame, first_batch: bool):
        write_mode = "a"
        if first_batch:
            write_mode = "w"
            os.makedirs(self.mapped_data_dir, exist_ok=True)
        try:
            gdf.to_file(
                filename=self.mapped_data_path,
                index=False,
                mode=write_mode,
                engine="fiona",
            )
        except Exception:
            shutil.rmtree(self.mapped_data_dir)
            raise

    def __zip_mapped_data(self):
        with ZipFile(self.zip_file_path, "w") as zipf:
            # Walk through all the files and subdirectories in the given directory
            for root, dirs, files in os.walk(self.mapped_data_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, self.mapped_data_dir)
                    zipf.write(file_path, arcname=relative_path)
