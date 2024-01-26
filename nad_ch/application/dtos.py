from dataclasses import dataclass


@dataclass
class DownloadResult:
    temp_dir: str
    extracted_dir: str
