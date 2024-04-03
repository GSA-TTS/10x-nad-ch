import click
from nad_ch.application.use_cases.data_producers import (
    add_data_producer,
    list_data_producers,
)
from nad_ch.application.use_cases.data_submissions import (
    ingest_data_submission,
    get_data_submissions_by_producer,
    validate_data_submission,
)


@click.group()
@click.pass_context
def cli(ctx):
    pass


@cli.command()
@click.pass_context
@click.argument("producer_name")
def add_producer(ctx, producer_name):
    context = ctx.obj
    add_data_producer(context, producer_name)


@cli.command()
@click.pass_context
def list_producers(ctx):
    context = ctx.obj
    list_data_producers(context)


@cli.command()
@click.pass_context
@click.argument("file_path")
@click.argument("producer")
def ingest(ctx, file_path, producer):
    context = ctx.obj
    ingest_data_submission(context, file_path, producer)


@cli.command()
@click.pass_context
@click.argument("producer")
def list_submissions_by_producer(ctx, producer):
    context = ctx.obj
    get_data_submissions_by_producer(context, producer)


@cli.command()
@click.pass_context
@click.argument("filename")
@click.argument("mapping_name")
def validate_submission(ctx, filename, mapping_name):
    context = ctx.obj
    validate_data_submission(context, filename, mapping_name)
