from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime
import re
from nad_ch.domain.entities import DataSubmission


@dataclass
class DataSubmissionViewModel:
    name: str
    date_created: str
    url: str


def present_data_submissions(
    submissions: Iterable[DataSubmission],
) -> Iterable[DataSubmissionViewModel]:
    view_models = []

    for submission in submissions:
        date_pattern = r"\d{8}_\d{6}"
        date_match = re.search(date_pattern, submission.filename)
        if date_match:
            date_str = date_match.group(0)
            date_created = datetime.strptime(date_str, "%Y%m%d_%H%M%S").strftime(
                "%B %d, %Y"
            )
        else:
            date_created = "Unknown"

        url = f"http://example.com/submissions/{submission.filename}"

        vm = DataSubmissionViewModel(
            name=submission.filename, date_created=date_created, url=url
        )
        view_models.append(vm)

    return view_models
