import click
from ..use_cases import ingest_data_submission


@click.group()
@click.pass_context
def cli(ctx):
    pass


@cli.command()
@click.pass_context
@click.argument('filepath')
@click.argument('provider')
def ingest(ctx, file_path, provider):
    context = ctx.obj
    ingest_data_submission(context, file_path, provider)
    click.echo("Ingest complete")
