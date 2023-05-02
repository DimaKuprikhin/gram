import pathlib


class Repository:
    app_name: str
    repo_owner: str
    repo_name: str
    path: pathlib.PosixPath

    def __init__(
        self,
        app_name: str,
        repo_owner: str,
        repo_name: str,
        path: pathlib.PosixPath
    ):
        self.app_name = app_name
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.path = path
