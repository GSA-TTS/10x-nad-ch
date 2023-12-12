import click
from ..use_cases import ingest_data_submission


@click.group()
@click.pass_context
def cli(ctx):
    pass


@cli.command()
@click.pass_context
@click.argument('file_path')
def ingest(ctx, file_path):
    context = ctx.obj
    ingest_data_submission(context, file_path)
    click.echo(f"Ingest complete")
