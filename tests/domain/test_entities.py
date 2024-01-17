import datetime
from nad_ch.domain.entities import DataProvider, DataSubmission


def test_data_submission_generates_filename():
    provider = DataProvider("Some Provider")
    filename = DataSubmission.generate_filename("someupload.zip", provider)
    todays_date = datetime.datetime.now().strftime("%Y%m%d")
    print(filename)
    assert filename.startswith("some_provider")
    assert todays_date in filename
    assert filename.endswith(".zip")
