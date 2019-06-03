import pathlib
import os
import json
import git


def get_current_head(root_path):
    repo = git.Repo(root_path)
    sha = repo.head.object.hexsha
    short_sha = repo.git.rev_parse(sha, short=7)

    return short_sha


def write_simple_info(run_config):

    config_folder_abs_path = run_config["environment"]["sentinel_config_root_path"]
    project_root_path = run_config["environment"]["version_control_root"]
    path = pathlib.Path(config_folder_abs_path)

    version_control_root_path = path.joinpath("_version_control")
    if not version_control_root_path.exists():
        os.makedirs(version_control_root_path)

    get_current_head(project_root_path)
    simple_info = {
        "commit_id": get_current_head(project_root_path)
    }

    version_control_file = version_control_root_path.joinpath("_vcs_info.json")
    f = open(version_control_file, "w")
    f.write(json.dumps(simple_info, indent=4))
    f.close()
