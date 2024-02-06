from dataclasses import dataclass, asdict


@dataclass
class DownloadResult:
    temp_dir: str
    extracted_dir: str


@dataclass
class DataSubmissionReport:
    feature_count: int

    def to_dict(self):
        return asdict(self)
