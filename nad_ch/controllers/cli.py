import click
from nad_ch.use_cases import (
    add_data_provider,
    list_data_providers,
    ingest_data_submission,
    list_data_submissions_by_provider
)


@click.group()
@click.pass_context
def cli(ctx):
    pass


@cli.command()
@click.pass_context
@click.argument('provider_name')
def add_provider(ctx, provider_name):
    context = ctx.obj
    add_data_provider(context, provider_name)


@cli.command()
@click.pass_context
def list_providers(ctx):
    context = ctx.obj
    list_data_providers(context)


@cli.command()
@click.pass_context
@click.argument('file_path')
@click.argument('provider')
def ingest(ctx, file_path, provider):
    context = ctx.obj
    ingest_data_submission(context, file_path, provider)


@cli.command()
@click.pass_context
@click.argument('provider')
def list_submissions_by_provider(ctx, provider):
    context = ctx.obj
    list_data_submissions_by_provider(context, provider)
