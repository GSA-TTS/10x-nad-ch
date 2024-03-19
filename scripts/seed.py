import os
import zipfile
from nad_ch.config import create_app_context, OAUTH2_CONFIG
from nad_ch.domain.entities import ColumnMap, DataProducer, DataSubmission, User


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
    )
    ctx.users.add(new_user)

    new_column_map = ColumnMap(
        name="NewJerseyMapping", producer=saved_producer, version_id=1
    )
    # TODO save column map once ApplicationContext can provide a repository
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
        "Post_City": "",
        "Census_Plc": "",
        "Uninc_Comm": "",
        "Nbrhd_Comm": "",
        "NatAmArea": "",
        "NatAmSub": "",
        "Urbnztn_PR": "",
        "PlaceOther": "",
        "PlaceNmTyp": "",
        "State": "state",
        "Zip_Code": "",
        "Plus_4": "",
        "UUID": "guid",
        "AddAuth": "",
        "AddrRefSys": "",
        "Longitude": "long",
        "Latitude": "lat",
        "NatGrid": "nat_grid",
        "Elevation": "",
        "Placement": "",
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
    gdb_path = os.path.join(
        project_root, "tests", "test_data", "geodatabases", "Naperville.gdb"
    )
    zipped_gdb_path = os.path.join(
        project_root, "tests", "test_data", "geodatabases", "Naperville.gdb.zip"
    )
    zip_directory(gdb_path, zipped_gdb_path)

    filename = DataSubmission.generate_filename(zipped_gdb_path, saved_producer)
    ctx.storage.upload(zipped_gdb_path, filename)
    new_submission = DataSubmission(filename, saved_producer, saved_column_map)
    ctx.submissions.add(new_submission)

    os.remove(zipped_gdb_path)


if __name__ == "__main__":
    main()
