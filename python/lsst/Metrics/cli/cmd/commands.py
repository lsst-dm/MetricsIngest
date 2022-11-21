#!/usr/bin/env python
"""
This is a standalone program to generate scripts
 used in creation and injection of production metrics.
"""
import click
from lsst.Metrics.MIUtils import MIUtils


@click.group()
def cli():
    """
    It is click grop main function.
    """
    pass


@cli.command()
@click.argument('name')
def make_js_file(name):
    """
    This is command to create make_json.sl file
    to be used in slurm to create production metrix json files.

    :parameter:
      name of the input yaml file containing configuration values.
      The structure of the file is in README.rst

    """
    click.echo('Start with make_js_file')
    mi = MIUtils(name)
    mi.make_json()
    click.echo('Created make_json.sl file')


@cli.command()
@click.argument('name')
def make_dispatch_sl(name):
    """
    This is command to create dispatch.sl file
    to be used in slurm to deploy metrix json files.

    :parameter:
      name of the input yaml file containing configuration values.
      The structure of the file is in README.rst

    """
    click.echo('Start with make_dispatch_sl')
    mi = MIUtils(name)
    mi.make_dispatch_sl()
    click.echo('Created dispatch.sl file')


@cli.command()
@click.argument('name')
def make_dispatch_sh(name):
    """
    This is command to create dispatch.sh file
    to be used in slurm together with dispatch.sl to deploy
     metrix json files.

    :parameter:
      name of the input yaml file containing configuration values.
      The structure of the file is in README.rst

    """
    click.echo('Start with make_dispatch_sh')
    mi = MIUtils(name)
    mi.make_dispatch_sh()
    click.echo('Created dispatch.sh file')


@cli.command()
@click.argument('name')
def make_steps(name):
    """
    This is command to create steps yaml files
    to be used  in panda submit command.

    :parameter:
      name of the input yaml file containing configuration values.
      The structure of the file is in README.rst

    """
    click.echo('Start with make_steps')
    mi = MIUtils(name)
    mi.make_steps()
    click.echo('Created step files file')


if __name__ == '__main__':
    cli()
