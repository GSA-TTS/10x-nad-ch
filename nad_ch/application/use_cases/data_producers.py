from typing import List
from nad_ch.application.interfaces import ApplicationContext
from nad_ch.application.view_models import (
    get_view_model,
    DataProducerViewModel,
)
from nad_ch.core.entities import DataProducer


def add_data_producer(
    ctx: ApplicationContext, producer_name: str
) -> DataProducerViewModel:
    if not producer_name:
        ctx.logger.error("Producer name required")
        return

    matching_producer = ctx.producers.get_by_name(producer_name)
    if matching_producer:
        ctx.logger.error("Producer name must be unique")
        return

    producer = DataProducer(producer_name)
    saved_producer = ctx.producers.add(producer)
    ctx.logger.info("Producer added")

    return get_view_model(saved_producer)


def list_data_producers(ctx: ApplicationContext) -> List[DataProducerViewModel]:
    producers = ctx.producers.get_all()
    ctx.logger.info("Data Producer Names:")
    for p in producers:
        ctx.logger.info(p.name)

    return get_view_model(producers)
