import click
from nad_ch.use_cases import add_data_provider, list_data_providers, ingest_data_submission, InvalidProviderNameException


@click.group()
@click.pass_context
def cli(ctx):
    pass


@cli.command()
@click.pass_context
@click.argument('provider_name')
def add_provider(ctx, provider_name):
    context = ctx.obj
    try:
        add_data_provider(context, provider_name)
    except InvalidProviderNameException as e:
        click.echo(f"Error: {e.message}")
        return

    click.echo('Provider added')


@cli.command()
@click.pass_context
def list_providers(ctx):
    context = ctx.obj
    providers = list_data_providers(context)
    click.echo('Data Provider Names:')
    for p in providers:
        click.echo(p.name)


@cli.command()
@click.pass_context
@click.argument('filepath')
@click.argument('provider')
def ingest(ctx, file_path, provider):
    context = ctx.obj
    ingest_data_submission(context, file_path, provider)
    click.echo('Ingest complete')
