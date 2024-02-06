from geopandas import GeoDataFrame


def get_feature_count(gdf: GeoDataFrame) -> int:
    return len(gdf)
