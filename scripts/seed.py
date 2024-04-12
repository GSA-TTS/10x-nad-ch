import os
import zipfile
from nad_ch.config import create_app_context, OAUTH2_CONFIG
from nad_ch.core.entities import (
    ColumnMap,
    DataProducer,
    DataSubmissionStatus,
    DataSubmission,
    User,
)


def zip_directory(folder_path, zip_path):
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                zipf.write(
                    os.path.join(root, file),
                    os.path.relpath(
                        os.path.join(root, file), os.path.join(folder_path, "..")
                    ),
                )


def main():
    if os.getenv("APP_ENV") != "dev_local":
        raise Exception("This script can only be run in a local dev environment.")

    ctx = create_app_context()

    new_producer = DataProducer(name="New Jersey")
    saved_producer = ctx.producers.add(new_producer)

    new_user = User(
        email="test@test.org",
        login_provider="cloudgov",
        logout_url=OAUTH2_CONFIG["cloudgov"]["logout_url"],
        producer=saved_producer,
        activated=True,
    )
    ctx.users.add(new_user)

    new_column_map = ColumnMap(
        name="NewJerseyMapping", producer=saved_producer, version_id=1
    )
    new_column_map.mapping = {
        "AddNum_Pre": "",
        "Add_Number": "address_number",
        "AddNum_Suf": "",
        "AddNo_Full": "address_number_full",
        "St_PreMod": "",
        "St_PreDir": "",
        "St_PreTyp": "",
        "St_PreSep": "",
        "St_Name": "street_name",
        "St_PosTyp": "",
        "St_PosDir": "",
        "St_PosMod": "",
        "StNam_Full": "street_name_full",
        "Building": "",
        "Floor": "",
        "Unit": "unit",
        "Room": "room",
        "Seat": "",
        "Addtl_Loc": "",
        "SubAddress": "",
        "LandmkName": "",
        "County": "county",
        "Inc_Muni": "city",
        "Post_City": "post_city",
        "Census_Plc": "",
        "Uninc_Comm": "",
        "Nbrhd_Comm": "",
        "NatAmArea": "",
        "NatAmSub": "",
        "Urbnztn_PR": "",
        "PlaceOther": "",
        "PlaceNmTyp": "",
        "State": "state",
        "Zip_Code": "zip",
        "Plus_4": "",
        "UUID": "guid",
        "AddAuth": "auth",
        "AddrRefSys": "",
        "Longitude": "long",
        "Latitude": "lat",
        "NatGrid": "nat_grid",
        "Elevation": "",
        "Placement": "placement",
        "AddrPoint": "address_point",
        "Related_ID": "",
        "RelateType": "",
        "ParcelSrc": "",
        "Parcel_ID": "",
        "AddrClass": "",
        "Lifecycle": "",
        "Effective": "",
        "Expire": "",
        "DateUpdate": "updated",
        "AnomStatus": "",
        "LocatnDesc": "",
        "Addr_Type": "",
        "DeliverTyp": "",
        "NAD_Source": "source",
        "DataSet_ID": "123456",
    }
    saved_column_map = ctx.column_maps.add(new_column_map)

    current_script_path = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_script_path))

    zipped_shapefile_path = os.path.join(
        project_root, "tests", "test_data", "shapefiles", "NM911_Address_202310.zip"
    )

    submission_name = "MorrisCounty2024A"
    file_path = DataSubmission.generate_zipped_file_path(submission_name, saved_producer)
    ctx.storage.upload(zipped_shapefile_path, file_path)
    report = {
        "overview": {
            "feature_count": 1141,
            "features_flagged": 0,
            "etl_update_required": False,
            "data_update_required": False,
        },
        "features": [
            {
                "provided_feature_name": "AddNum_Pre",
                "nad_feature_name": "AddNum_Pre",
                "populated_count": 1141,
                "null_count": 0,
                "required": False,
                "status": "No error",
            },
            {
                "provided_feature_name": "Add_Number",
                "nad_feature_name": "Add_Number",
                "populated_count": 1141,
                "null_count": 0,
                "required": True,
                "status": "No error",
            },
            {
                "provided_feature_name": "AddNum_Suf",
                "nad_feature_name": "AddNum_Suf",
                "populated_count": 1141,
                "null_count": 0,
                "required": False,
                "status": "No error",
            },
            {
                "provided_feature_name": "AddNo_Full",
                "nad_feature_name": "AddNo_Full",
                "populated_count": 1136,
                "null_count": 5,
                "required": True,
                "status": "Rejected",
            },
            {
                "provided_feature_name": "St_PreMod",
                "nad_feature_name": "St_PreMod",
                "populated_count": 604,
                "null_count": 537,
                "required": False,
                "status": "Custom ETL needed",
            },
            {
                "provided_feature_name": "St_Name",
                "nad_feature_name": "St_Name",
                "populated_count": 1141,
                "null_count": 0,
                "required": True,
                "status": "No error",
            },
            {
                "provided_feature_name": "StNam_Full",
                "nad_feature_name": "StNam_Full",
                "populated_count": 1141,
                "null_count": 0,
                "required": True,
                "status": "No error",
            },
            {
                "provided_feature_name": "County",
                "nad_feature_name": "County",
                "populated_count": 1140,
                "null_count": 1,
                "required": True,
                "status": "Rejected",
            },
            {
                "provided_feature_name": "Inc_Muni",
                "nad_feature_name": "Inc_Muni",
                "populated_count": 1141,
                "null_count": 0,
                "required": True,
                "status": "No error",
            },
            {
                "provided_feature_name": "State",
                "nad_feature_name": "State",
                "populated_count": 1141,
                "null_count": 0,
                "required": True,
                "status": "No error",
            },
            {
                "provided_feature_name": "UUID",
                "nad_feature_name": "UUID",
                "populated_count": 1141,
                "null_count": 0,
                "required": True,
                "status": "No error",
            },
            {
                "provided_feature_name": "Longitude",
                "nad_feature_name": "Longitude",
                "populated_count": 1141,
                "null_count": 0,
                "required": True,
                "status": "No error",
            },
            {
                "provided_feature_name": "Latitude",
                "nad_feature_name": "Latitude",
                "populated_count": 1141,
                "null_count": 0,
                "required": True,
                "status": "No error",
            },
            {
                "provided_feature_name": "NatGrid",
                "nad_feature_name": "NatGrid",
                "populated_count": 1130,
                "null_count": 11,
                "required": True,
                "status": "Updated by calculation",
            },
            {
                "provided_feature_name": "AddrPoint",
                "nad_feature_name": "AddrPoint",
                "populated_count": 1141,
                "null_count": 0,
                "required": True,
                "status": "No error",
            },
            {
                "provided_feature_name": "DateUpdate",
                "nad_feature_name": "DateUpdate",
                "populated_count": 1141,
                "null_count": 0,
                "required": True,
                "status": "No error",
            },
            {
                "provided_feature_name": "NAD_Source",
                "nad_feature_name": "NAD_Source",
                "populated_count": 0,
                "null_count": 1141,
                "required": True,
                "status": "Rejected",
            },
            {
                "provided_feature_name": "DataSet_ID",
                "nad_feature_name": "DataSet_ID",
                "populated_count": 0,
                "null_count": 1141,
                "required": True,
                "status": "Rejected",
            },
        ],
    }
    new_submission = DataSubmission(
        submission_name,
        file_path,
        DataSubmissionStatus.VALIDATED,
        saved_producer,
        saved_column_map,
        report,
    )
    ctx.submissions.add(new_submission)


if __name__ == "__main__":
    main()
