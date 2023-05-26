import pathlib


class Script:
    app_name: str
    path: pathlib.PosixPath

    def __init__(self, app_name: str, path: pathlib.PosixPath):
        self.app_name = app_name
        self.path = path.resolve()
