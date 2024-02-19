from dataclasses import dataclass
from datetime import datetime
import json
import numpy as np
from typing import Union, List, Tuple
from nad_ch.domain.entities import Entity, DataProducer, DataSubmission


def get_view_model(entity: Union[Entity, List[Entity]]) -> Union[Entity, List[Entity]]:
    """
    Provide a single factory function that an application use case can call in order to
    get a static view model object that it can return to its caller.
    """
    entity_to_vm_function_map = {
        DataProducer: create_data_producer_vm,
        DataSubmission: create_data_submission_vm,
    }

    # Check if the input is a list of entities
    if isinstance(entity, list):
        # Process each entity in the list using a list comprehension
        return [get_view_model(single_entity) for single_entity in entity]

    # Process a single entity
    entity_type = type(entity)
    if entity_type in entity_to_vm_function_map:
        mapping_function = entity_to_vm_function_map[entity_type]
        return mapping_function(entity)  # Call the mapping function for the entity
    else:
        raise ValueError(f"No mapping function defined for entity type: {entity_type}")


@dataclass
class DataProducerViewModel:
    id: int
    date_created: str
    name: str


def create_data_producer_vm(producer: DataProducer) -> DataProducerViewModel:
    return DataProducerViewModel(
        id=producer.id,
        date_created=present_date(producer.created_at),
        name=producer.name,
    )


@dataclass
class DataSubmissionViewModel:
    id: int
    date_created: str
    filename: str
    producer_name: str
    report: str


def create_data_submission_vm(submission: DataSubmission) -> DataSubmissionViewModel:
    # TODO make this be an empty array so the frontend doesn't have to check for None
    report_json = None
    if submission.report is not None:
        enriched_report = enrich_report(submission.report)
        report_json = json.dumps(enriched_report)

    return DataSubmissionViewModel(
        id=submission.id,
        date_created=present_date(submission.created_at),
        filename=submission.filename,
        producer_name=submission.producer.name,
        report=report_json,
    )


def enrich_report(report: dict) -> dict:
    required_fields = [
        "Add_Number",
        "AddNo_Full",
        "St_Name",
        "StName_Full",
        "County",
        "Inc_Muni",
        "Urbnztn_PR",
        "State",
        "UUID",
        "Longitude",
        "Latitude",
        "NatGrid",
        "AddrPoint",
        "DateUpdate",
        "NAD_Source",
        "DataSet_ID",
    ]

    for feature in report.get("features", []):
        percent_populated, percent_empty = calculate_percentages(
            feature.get("populated_count"), feature.get("null_count")
        )

        feature["populated_percentage"] = present_percentage(percent_populated)
        feature["null_percentage"] = present_percentage(percent_empty)

        nad_feature_name = feature.get("nad_feature_name")
        if nad_feature_name in required_fields:
            feature["required"] = True
        else:
            feature["required"] = False

    return report


def present_date(date: datetime) -> str:
    return date.strftime("%B %d, %Y")


def calculate_percentages(populated_count: int, null_count: int) -> Tuple[float, float]:
    total_fields = populated_count + null_count
    populated_percentage = (populated_count / total_fields) * 100
    null_percentage = (null_count / total_fields) * 100
    return populated_percentage, null_percentage


def present_percentage(percentage: float) -> str:
    rounded_percentage = np.around(percentage, 2)
    formatted_string = (
        f"{rounded_percentage:05.2f}%" if rounded_percentage != 0 else "00.00%"
    )
    return formatted_string
