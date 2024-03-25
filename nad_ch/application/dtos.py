from dataclasses import dataclass, asdict, field, is_dataclass
from typing import List, Dict
import numpy as np


@dataclass
class DownloadResult:
    temp_dir: str
    extracted_dir: str


@dataclass
class DataSubmissionReportOverview:
    feature_count: int = 0
    features_flagged: int = 0
    records_count: int = 0
    records_flagged: int = 0
    etl_update_required: bool = False
    data_update_required: bool = False
    missing_required_fields: List[str] = field(default_factory=list)


@dataclass
class DataSubmissionReportFeature:
    provided_feature_name: str
    nad_feature_name: str
    populated_count: int = 0
    null_count: int = 0
    invalid_domain_count: int = 0
    valid_domain_count: int = 0
    invalid_domains: List[str] = field(default_factory=list)
    domain_frequency: Dict[str, Dict[str, int]] = field(default_factory=dict)
    # Set to true when there is too many unexpected domain values found for a field
    high_domain_cardinality: bool = False


@dataclass
class DataSubmissionReport:
    overview: DataSubmissionReportOverview
    features: List[DataSubmissionReportFeature] = field(default_factory=list)


def report_to_dict(data_submission_report: DataSubmissionReport) -> dict:
    """
    Converts a DataSubmissionReport instance into a dictionary because all data types
    within the dictionary must be JSON-serializable.
    """
    return convert(asdict(data_submission_report))


def report_from_dict(data: dict) -> DataSubmissionReport:
    """
    Creates a DataSubmissionReport instance from a dictionary, reconstructing the
    overview and features properties from their respective dictionary representations.
    """

    overview_data = data.get("overview", {})
    features_data = data.get("features", [])

    overview = DataSubmissionReportOverview(**overview_data)
    features = [
        DataSubmissionReportFeature(**feature_data) for feature_data in features_data
    ]

    return DataSubmissionReport(overview=overview, features=features)


def convert(item):
    """
    Recursively converts items within a data structure (including dictionaries, lists,
    and dataclass instances) such that all numeric types are JSON-serializable.
    """
    if isinstance(item, dict):
        return {k: convert(v) for k, v in item.items()}
    elif isinstance(item, list):
        return [convert(i) for i in item]
    elif isinstance(item, (np.int64, np.int32, np.float64, np.float32)):
        return int(item) if isinstance(item, (np.int64, np.int32)) else float(item)
    elif is_dataclass(item):
        return convert(asdict(item))
    else:
        return item
