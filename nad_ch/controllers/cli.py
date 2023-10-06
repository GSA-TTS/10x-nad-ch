import click
from ..entities import File
from ..use_cases import upload_file, list_files, get_file_metadata

@click.group()
@click.pass_context
def cli(ctx):
    pass

@cli.command()
@click.pass_context
@click.argument('filename')
@click.argument('content')
def upload(ctx, filename, content):
    context = ctx.obj
    file = File(name=filename, content=content)
    upload_file(context, file)
    click.echo(f"Uploaded {filename}")

@cli.command()
@click.pass_context
def listall(ctx):
    context = ctx.obj
    files = list_files(context)
    for file in files:
        click.echo(file.name)

@cli.command()
@click.pass_context
@click.argument('filename')
def metadata(ctx, filename):
    context = ctx.obj
    metadata = get_file_metadata(context, filename)
    click.echo(f"File: {metadata.name}, Size: {metadata.size} bytes")
