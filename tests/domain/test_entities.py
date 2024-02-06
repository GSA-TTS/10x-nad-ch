import datetime
from nad_ch.domain.entities import DataProvider, DataSubmission


def test_data_submission_generates_filename():
    provider = DataProvider("Some Provider")
    filename = DataSubmission.generate_filename("someupload.zip", provider)
    todays_date = datetime.datetime.now().strftime("%Y%m%d")
    assert filename.startswith("some_provider_")
    assert todays_date in filename
    assert filename.endswith(".zip")


def test_data_submission_knows_if_it_has_a_report():
    report_data = {"key1": "value1", "key2": "value2"}
    submission = DataSubmission(
        "someupload.zip", DataProvider("Some provider"), report_data
    )
    assert submission.has_report() == True


def test_data_submission_knows_if_it_does_not_have_a_report():
    submission = DataSubmission("someupload.zip", DataProvider("Some provider"))
    assert submission.has_report() == False
