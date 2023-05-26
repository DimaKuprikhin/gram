import sqlite3
import pathlib
import typing

from models.application import Application


CHECK_TABLE_QUERY = (
    '''SELECT name FROM sqlite_master
    WHERE type=\'table\' AND name=\'applications\';'''
)
CREATE_TABLE_QUERY = (
    '''CREATE TABLE applications (
        app_name TEXT PRIMARY KEY,
        current_version TEXT NOT NULL,
        repo_owner TEXT NOT NULL,
        repo_name TEXT NOT NULL,
        branch TEXT NOT NULL
    );'''
)
INSERT_QUERY = (
    '''INSERT INTO applications (
        app_name,
        current_version,
        repo_owner,
        repo_name,
        branch
    )
    VALUES (?, ?, ?, ?, ?);'''
)
SELECT_QUERY = (
    '''SELECT app_name, current_version, repo_owner, repo_name, branch
    FROM applications
    WHERE app_name = ?;'''
)
SELECT_ALL_QUERY = (
    '''SELECT app_name, current_version, repo_owner, repo_name, branch
    FROM applications;'''
)
DELETE_QUERY = (
    '''DELETE FROM applications
    WHERE app_name = ?;'''
)
UPDATE_QUERY = (
    '''UPDATE applications
    SET (current_version, repo_owner, repo_name, branch) = (?, ?, ?, ?)
    WHERE app_name = ?;'''
)


class ApplicationsDB:
    path: pathlib.PosixPath

    def __init__(self, db_path: pathlib.PosixPath):
        self.path = db_path.resolve()
        self.conn = sqlite3.connect(self.path)
        if not self.is_initialized():
            self.initialize()

    def is_initialized(self) -> bool:
        cur = self.conn.cursor()
        res = cur.execute(CHECK_TABLE_QUERY)
        return res.fetchone() is not None

    def initialize(self):
        cur = self.conn.cursor()
        cur.execute(CREATE_TABLE_QUERY)
        self.conn.commit()

    def add(self, app: Application):
        cur = self.conn.cursor()
        cur.execute(
            INSERT_QUERY,
            [
                app.app_name,
                app.current_version,
                app.repo_owner,
                app.repo_name,
                app.branch,
            ]
        )
        self.conn.commit()

    def get(self, app_name: str) -> typing.Optional[Application]:
        cur = self.conn.cursor()
        res = cur.execute(SELECT_QUERY, [app_name]).fetchone()
        if res is None:
            return None
        return Application(res[0], int(res[1]), res[2], res[3], res[4])

    def update(self, app: Application):
        cur = self.conn.cursor()
        cur.execute(
            UPDATE_QUERY,
            [
                app.current_version,
                app.repo_owner,
                app.repo_name,
                app.branch,
                app.app_name
            ],
        )
        self.conn.commit()

    def list(self) -> typing.List[Application]:
        cur = self.conn.cursor()
        res = cur.execute(SELECT_ALL_QUERY).fetchall()
        repositories: typing.List[Application] = []
        for row in res:
            repositories.append(Application(
                row[0], int(row[1]), row[2], row[3], row[4]))
        return repositories

    def remove(self, app_name: str) -> bool:
        cur = self.conn.cursor()
        cur.execute(DELETE_QUERY, app_name)
        self.conn.commit()
        return cur.rowcount >= 1
