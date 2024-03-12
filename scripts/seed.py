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

    # new_column_map = ColumnMap(name="New Jersey Mapping v1", producer=saved_producer)
    # TODO save column map once ApplicationContext can provide a repository
    # saved_column_map = ctx.column_maps.add(new_column_map)

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
    # TODO save submission once column map has been saved to disk
    # new_submission = DataSubmission(filename, saved_producer, saved_column_map)
    # ctx.submissions.add(new_submission)

    os.remove(zipped_gdb_path)


if __name__ == "__main__":
    main()
