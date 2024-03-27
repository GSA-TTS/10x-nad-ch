import csv
from io import StringIO
from typing import Dict, List, IO
from nad_ch.application.interfaces import ApplicationContext
from nad_ch.application.view_models import (
    get_view_model,
    ColumnMapViewModel,
)
from nad_ch.core.entities import ColumnMap


def add_column_map(
    ctx: ApplicationContext, user_id: int, name: str, mapping: Dict[str, str]
):
    user = ctx.users.get_by_id(user_id)
    if user is None:
        raise ValueError("User not found")

    # TODO get the producer name from the user's producer property
    producer = user.producer
    if producer is None:
        raise ValueError("Producer not found")

    # Note: will need to account for admin permissions to update any DataProducer's
    # column mapping, and for users associated with the DataProducer to update ONLY
    # their own column mapping

    column_map = ColumnMap(name, producer, mapping, 1)

    if not column_map.is_valid():
        raise ValueError("Invalid mapping")

    saved_column_map = ctx.column_maps.add(column_map)
    ctx.logger.info("Column Map added")

    return get_view_model(saved_column_map)


def get_column_map(ctx: ApplicationContext, id: int) -> ColumnMapViewModel:
    column_map = ctx.column_maps.get_by_id(id)

    if column_map is None:
        raise ValueError("Column map not found")

    return get_view_model(column_map)


def get_column_maps_by_producer(
    ctx: ApplicationContext, producer_name: str
) -> List[ColumnMapViewModel]:
    producer = ctx.producers.get_by_name(producer_name)
    if not producer:
        raise ValueError("Producer not found")
    column_maps = ctx.column_maps.get_by_producer(producer)

    return [get_view_model(column_map) for column_map in column_maps]


def update_column_mapping(
    ctx: ApplicationContext, id: int, new_mapping: Dict[str, str]
):
    column_map = ctx.column_maps.get_by_id(id)

    if column_map is None:
        raise ValueError("Column map not found")

    column_map.mapping = {
        key: new_mapping[key] for key in ColumnMap.all_fields if key in new_mapping
    }

    if not column_map.is_valid():
        raise ValueError("Invalid mapping")

    ctx.column_maps.update(column_map)

    return get_view_model(column_map)


def update_column_mapping_field(
    ctx: ApplicationContext, id: int, user_field: str, nad_field: str
):
    column_map = ctx.column_maps.get_by_id(id)

    if column_map is None:
        raise ValueError("Column map not found")

    column_map.mapping[nad_field] = user_field

    column_map.mapping = {
        key: column_map.mapping[key]
        for key in ColumnMap.all_fields
        if key in column_map.mapping
    }

    if not column_map.is_valid():
        raise ValueError("Invalid mapping")

    ctx.column_maps.update(column_map)

    return get_view_model(column_map)


def get_column_map_from_csv_file(file: IO[bytes]) -> Dict[str, str]:
    file_content = file.read().decode("utf-8-sig")
    stream = StringIO(file_content)
    csv_reader = csv.reader(stream, dialect="excel")

    headers = next(csv_reader)
    if not headers:
        raise Exception("CSV file is empty or invalid")

    csv_dict = {}

    for row in csv_reader:
        if len(row) < 2:
            continue
        key, value = row[:2]
        csv_dict[key] = value

    return csv_dict
