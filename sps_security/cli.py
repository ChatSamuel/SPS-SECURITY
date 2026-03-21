import click
from sps_security.ui.shell import start_shell
from sps_security.actions.cloud_action import run_cloud


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        start_shell()


@cli.command()
@click.argument("file")
def cloud(file):
    run_cloud(file)


def run():
    cli()
