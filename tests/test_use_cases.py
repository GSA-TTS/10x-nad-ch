import pytest
from nad_ch.application_context import create_app_context
from nad_ch.entities import File, FileMetadata
from nad_ch.use_cases import upload_file, list_files, get_file_metadata

@pytest.fixture(scope="function")
def app_context():
    context = create_app_context()
    yield context

def test_upload_file(app_context):
    file = File(name="test.txt", content="Sample content")

    upload_file(app_context, file)

    stored_file = app_context.storage.get_file("test.txt")
    assert stored_file.name == "test.txt"
    assert stored_file.content == "Sample content"

def test_list_files(app_context):
    file1 = File(name="test1.txt", content="Content 1")
    file2 = File(name="test2.txt", content="Content 2")
    upload_file(app_context, file1)
    upload_file(app_context, file2)

    files = list_files(app_context)

    assert len(files) == 2
    assert any(f.name == "test1.txt" for f in files)
    assert any(f.name == "test2.txt" for f in files)

def test_get_file_metadata(app_context):
    file = File(name="test.txt", content="Sample content for metadata")
    upload_file(app_context, file)

    metadata = get_file_metadata(app_context, "test.txt")

    assert isinstance(metadata, FileMetadata)
