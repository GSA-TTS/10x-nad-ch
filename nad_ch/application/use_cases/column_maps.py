import json
from nad_ch.application.interfaces import ApplicationContext
from nad_ch.application.view_models import (
    get_view_model,
    ColumnMapViewModel,
)
from nad_ch.domain.entities import ColumnMap


def add_column_map(ctx: ApplicationContext, user_id: int, name: str, mapping_string: str):
    user = ctx.users.get_by_id(user_id)
    if user is None:
        raise ValueError("User not found")

    producer = ctx.producers.get_by_name("New Jersey")
    if producer is None:
        raise ValueError("Producer not found")

    column_map = ColumnMap(name, producer, mapping_string, 1)

    if not column_map.is_valid():
        raise ValueError("Invalid mapping")

    saved_column_map = ctx.column_maps.add(column_map)
    ctx.logger.info("Column Map added")

    return get_view_model(saved_column_map)


def get_column_map(ctx: ApplicationContext, id: int) -> ColumnMapViewModel:
    column_map = ctx.column_maps.get_by_id(id)

    if column_map is None:
        return None

    return get_view_model(column_map)


def get_column_maps_by_provider(ctx: ApplicationContext, producer_id: int) -> list[ColumnMapViewModel]:
    pass
    # column_maps = ctx.column_maps.get_by_producer_id(producer_id)

    # return [get_view_model(column_map) for column_map in column_maps]
