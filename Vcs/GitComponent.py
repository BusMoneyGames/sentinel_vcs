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

    version_control_root_path = path.joinpath("gen_version_control")

    if not version_control_root_path.exists():
        os.makedirs(version_control_root_path)

    get_current_head(project_root_path)

    simple_info = {
        "commit_id": get_current_head(project_root_path)
    }

    version_control_file = version_control_root_path.joinpath("gen_vcs_info.json")

    f = open(version_control_file, "w")
    f.write(json.dumps(simple_info, indent=4))
    f.close()


class GitRepoWalker:

    def __init__(self, environment_config):
        project_root_path = environment_config["environment"]["version_control_root"]

        self.repo = git.Repo(project_root_path)
        self.commits = self._get_commit_history()

    def _clean_repo(self):
        self.repo.git.reset("--hard")
        self.repo.git.clean("-dfx")

    def clean_checkout_commit(self, commit_id):
        self._clean_repo()
        self.repo.git.checkout(commit_id)

    def _get_commit_history(self):
        commits = []
        for commit in self.repo.iter_commits():
            commits.append(commit)

        return commits

