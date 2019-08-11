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


def write_history_file(environment_config, commit_id):
    """
    Writes an info file about the commit
    """

    walker = GitRepoWalker(environment_config)

    path = pathlib.Path(environment_config["environment"]["sentinel_artifacts_path"]).joinpath("vcs_info.json")
    entry = walker.get_entry_from_commit_id(commit_id)

    f = open(path, "w")
    f.write(json.dumps(entry, indent=4))
    f.close()


class GitRepoWalker:

    def __init__(self, environment_config):
        project_root_path = environment_config["environment"]["version_control_root"]

        self.repo = git.Repo(project_root_path)
        self.commits = []
        self.commit_ids = []
        self.history = self._construct_git_history()
        self.current_commit = ""

    def _clean_repo(self):
        self.repo.git.reset("--hard")
        self.repo.git.clean("-dfx")

    def clean_checkout_commit(self, commit_id):
        self._clean_repo()
        self.repo.git.checkout(commit_id)

        self.current_commit = commit_id

    @staticmethod
    def _create_json_entry_for_commit(commit):

        entry = {"commit_time": str(commit.committed_datetime),
                 "commit_sha": str(commit.hexsha),
                 "comitter": str(commit.committer),
                 "message": commit.message,
                 "changes": commit.stats.files}

        return entry

    def get_entry_from_commit_id(self, commit_id):

        entry = ""
        for commit in self.repo.iter_commits():
            if str(commit.hexsha).startswith(commit_id):
                entry = self._create_json_entry_for_commit(commit)
                break

        if not entry:
            print("Error: %s not found in history", commit_id)

        return entry

    def _construct_git_history(self):

        root = {}
        for commit in self.repo.iter_commits():
            root[commit.hexsha] = self._create_json_entry_for_commit(commit)

            # Todo refactor whatever uses the commits to user the json file
            self.commits.append(commit)
            self.commit_ids.append(commit.hexsha)

        return root
