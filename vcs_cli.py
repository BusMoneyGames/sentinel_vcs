import logging
import pathlib
from pprint import pprint
import click
import json
from Vcs import GitComponent

def _read_config(path):
    """Reads the assembled config"""

    if path.exists():
        f = open(path, "r")
        config = json.load(f)
        f.close()

        return config
    else:
        print(f"No config found at {path}")
        print("Exiting!")
        quit(1)


def get_config_path(ctx):
    """Construct the config dict path"""
    return pathlib.Path(ctx.obj['PROJECT_ROOT']).joinpath("_generated_sentinel_config.json")


def get_config(ctx):
    """Return the environment config dict"""
    return _read_config(get_config_path(ctx))

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
def update_config(ctx, output):
    """Updates sentinel config with the relevant information"""

    GitComponent.update_sentinel_config(get_config(ctx))


@cli.command()
@click.option('-o', '--output', type=click.Choice(['text', 'json']), default='text', help="Output type.")
@click.pass_context
def list_modified_files(ctx, output):
    """Return files that have been changed in workspace"""

    modified_files = GitComponent.get_modified_files(get_config(ctx))

    print(json.dumps(modified_files, indent=4))


@cli.command()
@click.option('-o', '--output', type=click.Choice(['text', 'json']), default='text', help="Output type.")
@click.pass_context
def list_submodules(ctx, output):
    """Return a list of submodules in project"""

    submodules = GitComponent.list_submodules(get_config(ctx))

    print(json.dumps(submodules, indent=4))

@cli.command()
@click.pass_context
def find_missing_commits(ctx):
    # TODO make this do something
    walker = GitComponent.GitRepoWalker(get_config(ctx))


@cli.command()
@click.option('--short', is_flag=True, help="return as short commit")
@click.option('-o', '--output', type=click.Choice(['text', 'json']), default='text', help="Output type.")
@click.pass_context
def get_commit_id(ctx, short, output):

    config = get_config(ctx)
    git_info = GitComponent.GitInfo(config)
    commitID = git_info.get_commit_id(short)

    if output == 'json':
        pprint({"commitID":commitID})
    elif output == 'text':
        print(commitID)



if __name__ == "__main__":
    cli()
