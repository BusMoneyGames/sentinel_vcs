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


def _load_environment_config(overwrite_path=""):
    """Finds the config file that contains the environment information"""
    # Figure out where the script is run from
    current_run_directory = pathlib.Path(os.getcwd())
    L.debug("Current Directory: %s ", current_run_directory)

    if overwrite_path:
        L.debug("environment config read from none default location")
        L.debug("relative environment path is: %s", overwrite_path)
    else:
        overwrite_path = ".."
        L.debug("Using the default relative path that resolves to:  %s", overwrite_path)

    config_file_name = "_sentinel_root.json"
    config_file_path = current_run_directory.joinpath(overwrite_path, config_file_name).resolve()
    L.debug("Searching for environment file at: %s", config_file_path)
    L.debug("environment file exists: %s ", config_file_path.exists())

    if config_file_path.exists():
        return config_file_path
    else:
        L.error("Unable to find config environment file")
        L.error("Expected Path: %s", config_file_path)
        quit(1)


@click.group()
@click.option('--path', default="", help="path to the config overwrite folder")
@click.option('--debug', default=False, help="Turns on debug messages")
@click.pass_context
def cli(ctx, path, debug):
    """Sentinel Unreal Component handles running commands interacting with unreal engine"""

    ctx.ensure_object(dict)
    ctx.obj['CONFIG_OVERWRITE'] = path

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

    config_path = ctx.obj['CONFIG_OVERWRITE']

    sentinel_environment_config = _load_environment_config(config_path)

    environment_config = _read_config(sentinel_environment_config)
    GitComponent.write_simple_info(environment_config)


if __name__ == "__main__":
    cli()
