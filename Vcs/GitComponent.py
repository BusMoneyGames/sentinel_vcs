import pathlib
import os
import json

def write_simple_info(run_config):
    config_folder_abs_path = run_config["environment"]["sentinel_config_root_path"]
    path = pathlib.Path(config_folder_abs_path)

    version_control_root_path = path.joinpath("_version_control")
    if not version_control_root_path.exists():
        os.makedirs(version_control_root_path)

    simple_info = {"commit_id": "adfadfadsfa"}

    version_control_file = version_control_root_path.joinpath("vcs_info.json")
    f = open(version_control_file, "w")
    f.write(json.dumps(simple_info, indent=4))
    f.close()
