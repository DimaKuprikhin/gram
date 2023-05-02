import sqlite3
import pathlib
import typing

from models.repository import Repository


CHECK_TABLE_QUERY = (
    '''SELECT name FROM sqlite_master
    WHERE type=\'table\' AND name=\'repositories\';'''
)
CREATE_TABLE_QUERY = (
    '''CREATE TABLE repositories (
        app_name TEXT PRIMARY KEY,
        repo_owner TEXT NOT NULL,
        repo_name TEXT NOT NULL,
        path TEXT NOT NULL
    );'''
)
INSERT_QUERY = (
    '''INSERT INTO repositories (app_name, repo_owner, repo_name, path)
    VALUES (?, ?, ?, ?);'''
)
SELECT_QUERY = (
    '''SELECT app_name, repo_owner, repo_name, path
    FROM repositories
    WHERE app_name = ?;'''
)
SELECT_ALL_QUERY = (
    '''SELECT app_name, repo_owner, repo_name, path
    FROM repositories;'''
)
DELETE_QUERY = (
    '''DELETE FROM repositories
    WHERE app_name = ?;'''
)


class RepositoriesDB:
    path: pathlib.PosixPath

    def __init__(self, db_path: pathlib.PosixPath):
        self.path = db_path.resolve()
        self.conn = sqlite3.connect(self.path)

    def is_initialized(self) -> bool:
        cur = self.conn.cursor()
        res = cur.execute(CHECK_TABLE_QUERY)
        return res.fetchone() is not None

    def initialize(self):
        cur = self.conn.cursor()
        cur.execute(CREATE_TABLE_QUERY)
        self.conn.commit()

    def add(self, repository: Repository):
        cur = self.conn.cursor()
        cur.execute(
            INSERT_QUERY,
            [
                repository.app_name,
                repository.repo_owner,
                repository.repo_name,
                str(repository.path.resolve())
            ]
        )
        self.conn.commit()

    def get(self, app_name: str) -> typing.Optional[Repository]:
        cur = self.conn.cursor()
        res = cur.execute(SELECT_QUERY, [app_name]).fetchone()
        if res is None:
            return None
        return Repository(res[0], res[1], res[2], pathlib.PosixPath(res[3]))

    def list(self) -> typing.List[Repository]:
        cur = self.conn.cursor()
        res = cur.execute(SELECT_ALL_QUERY).fetchall()
        repositories: typing.List[Repository] = []
        for row in res:
            repositories.append(Repository(
                row[0], row[1], row[2], pathlib.PosixPath(row[3])))
        return repositories

    def remove(self, app_name: str) -> bool:
        cur = self.conn.cursor()
        cur.execute(DELETE_QUERY, app_name)
        self.conn.commit()
        return cur.rowcount >= 1
