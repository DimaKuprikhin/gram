import pathlib
import typing

from databases.repositories_db import RepositoriesDB
from models.repository import Repository
import utils


class RepositoryManager:
    db: RepositoriesDB
    dir: pathlib.PosixPath
    repos_dir: pathlib.PosixPath

    def __init__(self, dir: pathlib.PosixPath):
        self.dir = dir.resolve()
        if not self.dir.exists():
            self.dir.mkdir(parents=True)

        self.repos_dir = self.dir / 'repos'
        if not self.repos_dir.exists():
            self.repos_dir.mkdir()

        self._init_db()

    def _init_db(self):
        self.db = RepositoriesDB(self.dir / 'repositories.db')
        if not self.db.is_initialized():
            self.db.initialize()

    def add(self, app_name: str, url: str):
        owner, name = utils.parse_github_url(url)
        repository = Repository(app_name, owner, name, self.repos_dir / app_name)
        utils.rmdir(repository.path)
        repository.path.mkdir()
        utils.download_repo(
            repository.repo_owner,
            repository.repo_name,
            repository.path
        )
        self.db.add(repository)

    def get(self, app_name: str)-> typing.Optional[Repository]:
        return self.db.get(app_name)

    def remove(self, app_name: str)-> bool:
        repository = self.db.get(app_name)
        utils.rmdir(repository.path)
        return self.db.remove(app_name)

    def list(self)-> typing.List[Repository]:
        return self.db.list()
