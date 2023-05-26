class Application:
    app_name: str
    current_version: int
    repo_owner: str
    repo_name: str
    branch: str

    def __init__(
        self,
        app_name: str,
        current_version: int,
        repo_owner: str,
        repo_name: str,
        branch: str
    ):
        self.app_name = app_name
        self.current_version = current_version
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.branch = branch
