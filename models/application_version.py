import datetime
import pathlib


class ApplicationVersion:
    app_name: str
    version: int
    installed_at: datetime.datetime
    commit: str
    path: pathlib.PosixPath
    is_downloaded: bool

    def __init__(
        self,
        app_name: str,
        version: int,
        installed_at: datetime.datetime,
        commit: str,
        path: pathlib.PosixPath,
        is_downloaded: bool,
    ):
        self.app_name = app_name
        self.version = version
        self.installed_at = installed_at
        self.commit = commit
        self.path = path
        self.is_downloaded = is_downloaded
