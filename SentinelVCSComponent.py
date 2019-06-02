import logging
import pathlib
import click
import json
from Vcs import GitComponent
import os

L = logging.getLogger()


def _read_config(path):
    """Reads the assembled config"""

    L.debug("Reading config from: %s - Exists: %s", path, path.exists())

    if path.exists():
        f = open(path, "r")
        config = json.load(f)
        f.close()

        return config
    else:
        L.error("Unable to find generated config at: %s ", path)
        quit(1)


@click.group()
@click.option('--project_root', default="", help="path to the config overwrite folder")
@click.option('--debug', default=False, help="Turns on debug messages")
@click.pass_context
def cli(ctx, project_root, debug):
    """Sentinel Unreal Component handles running commands interacting with unreal engine"""

    ctx.ensure_object(dict)
    ctx.obj['PROJECT_ROOT'] = project_root

    if debug:
        L.setLevel(logging.DEBUG)
        message_format = '%(levelname)s - %(message)s '
    else:
        message_format = '%(levelname)s %(message)s '
        L.setLevel(logging.ERROR)

    logging.basicConfig(format=message_format)


@cli.command()
@click.option('-o', '--output', type=click.Choice(['text', 'json']), default='text', help="Output type.")
@click.pass_context
def refresh(ctx, output):
    """Generates a config file """

    config_path = pathlib.Path(ctx.obj['PROJECT_ROOT']).joinpath("_generated_sentinel_config.json")
    environment_config = _read_config(config_path)
    GitComponent.write_simple_info(environment_config)


if __name__ == "__main__":
    cli()
