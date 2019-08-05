import logging
import pathlib
import click
import json
from Vcs import GitComponent

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
@click.option('--project_root', default="", help="Path to the config overwrite folder")
@click.option('--output', type=click.Choice(['text', 'json']), default='text', help="Output type.")
@click.option('--no_version', type=click.Choice(['true', 'false']), default='true', help="Skips output version")
@click.option('--debug', type=click.Choice(['true', 'false']), default='false', help="Verbose logging")
@click.pass_context
def cli(ctx, project_root, output, no_version, debug):
    """Sentinel Unreal Component handles running commands interacting with unreal engine"""

    ctx.ensure_object(dict)
    ctx.obj['PROJECT_ROOT'] = project_root


@cli.command()
@click.option('-o', '--output', type=click.Choice(['text', 'json']), default='text', help="Output type.")
@click.pass_context
def refresh(ctx, output):
    """Generates a config file """

    config_path = pathlib.Path(ctx.obj['PROJECT_ROOT']).joinpath("_generated_sentinel_config.json")
    environment_config = _read_config(config_path)
    GitComponent.write_simple_info(environment_config)


@cli.command()
@click.option('-o', '--output', type=click.Choice(['text', 'json']), default='text', help="Output type.")
@click.option('--commit_id', help="Commit ID")
@click.pass_context
def write_history_file(ctx, output, commit_id):
    """Generates a config file """

    config_path = pathlib.Path(ctx.obj['PROJECT_ROOT']).joinpath("_generated_sentinel_config.json")
    environment_config = _read_config(config_path)
    GitComponent.write_history_file(environment_config, commit_id)


@cli.command()
@click.pass_context
def find_missing_commits(ctx):
    config_path = pathlib.Path(ctx.obj['PROJECT_ROOT']).joinpath("_generated_sentinel_config.json")
    environment_config = _read_config(config_path)
    walker = GitComponent.GitRepoWalker(environment_config)



if __name__ == "__main__":
    cli()
