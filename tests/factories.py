import geopandas as gpd
import pandas as pd
import numpy as np
from uuid import uuid4


def create_fake_geopandas_dataframe(num_rows=10):
    # Generate random data
    data = {
        "AddNum_Pre": [None] * num_rows,
        "Add_Number": np.random.randint(1, 100, size=num_rows),
        "AddNum_Suf": [None] * num_rows,
        "AddNo_Full": [str(np.random.randint(1, 100)) for _ in range(num_rows)],
        "St_PreMod": [None] * num_rows,
        "St_PreDir": ["South"] * num_rows,
        "St_PreTyp": [None] * num_rows,
        "St_PreSep": [None] * num_rows,
        "St_Name": ["Street{}".format(i) for i in range(num_rows)],
        "St_PosTyp": ["Street"] * num_rows,
        "St_PosDir": [None] * num_rows,
        "St_PosMod": [None] * num_rows,
        "StNam_Full": ["South Street{}".format(i) for i in range(num_rows)],
        "Building": [None] * num_rows,
        "Floor": [None] * num_rows,
        "Unit": [None] * num_rows,
        "Room": [None] * num_rows,
        "Seat": [None] * num_rows,
        "Addtl_Loc": [None] * num_rows,
        "SubAddress": [None] * num_rows,
        "LandmkName": [None] * num_rows,
        "County": ["Anycounty"] * num_rows,
        "Inc_Muni": ["Anytown"] * num_rows,
        "Post_City": ["Anytown"] * num_rows,
        "State": ["IN"] * num_rows,
        "Zip_Code": [str(np.random.randint(10000, 99999)) for _ in range(num_rows)],
        "UUID": [str(uuid4()) for _ in range(num_rows)],
        "AddAuth": ["Anycounty County"] * num_rows,
        "Longitude": np.random.uniform(low=-180, high=180, size=num_rows),
        "Latitude": np.random.uniform(low=-90, high=90, size=num_rows),
        "Placement": ["Structure - Rooftop"] * num_rows,
        "DateUpdate": [pd.Timestamp.now() for _ in range(num_rows)],
        "Addr_Type": ["Commercial"] * num_rows,
        "NAD_Source": ["Indiana State Library"] * num_rows,
        "DataSet_ID": [str(uuid4()) for _ in range(num_rows)],
    }

    # Create DataFrame
    df = pd.DataFrame(data)

    # Create GeoDataFrame
    gdf = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df["Longitude"], df["Latitude"])
    )

    # Set GeoJSON metadata
    gdf_metadata = {
        "type": "FeatureCollection",
        "crs": {
            "type": "name",
            "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"},
        },
    }
    gdf.__geo_interface__["metadata"] = gdf_metadata

    return gdf
