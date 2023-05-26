import datetime
import sqlite3
import pathlib
import typing

from models.application_version import ApplicationVersion


CHECK_TABLE_QUERY = (
    '''SELECT name FROM sqlite_master
    WHERE type=\'table\' AND name=\'application_versions\';'''
)
CREATE_TABLE_QUERY = (
    '''CREATE TABLE application_versions (
        app_name TEXT NOT NULL,
        version INTEGER NOT NULL,
        installed_at INTEGER NOT NULL,
        commit_ TEXT NOT NULL,
        path TEXT NOT NULL,
        is_downloaded BOOLEAN NOT NULL,
        PRIMARY KEY (app_name, version)
    );'''
)
INSERT_QUERY = (
    '''INSERT INTO application_versions (
        app_name,
        version,
        installed_at,
        commit_,
        path,
        is_downloaded
    )
    VALUES (?, ?, ?, ?, ?, ?);'''
)
SELECT_QUERY = (
    '''SELECT app_name, version, installed_at, commit_, path, is_downloaded
    FROM application_versions
    WHERE (app_name, version) = (?, ?);'''
)
SELECT_ALL_QUERY = (
    '''SELECT app_name, version, installed_at, commit_, path, is_downloaded
    FROM application_versions;'''
)
DELETE_QUERY = (
    '''DELETE FROM application_versions
    WHERE (app_name, version) = (?, ?);'''
)
UPDATE_QUERY = (
    '''UPDATE application_versions
    SET (installed_at, commit_, path, is_downloaded) = (?, ?, ?, ?, ?)
    WHERE (app_name, version) = (?, ?);'''
)


def _deserialize_application_version(row) -> ApplicationVersion:
    return ApplicationVersion(
        row[0],
        row[1],
        datetime.datetime.fromtimestamp(row[2].__int__()),
        row[3],
        pathlib.PosixPath(row[4]),
        row[5],
    )


class ApplicationVersionsDB:
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

    def add(self, app_version: ApplicationVersion):
        cur = self.conn.cursor()
        cur.execute(
            INSERT_QUERY,
            [
                app_version.app_name,
                app_version.version,
                app_version.installed_at.timestamp().__int__(),
                app_version.commit,
                app_version.path.resolve().__str__(),
                app_version.is_downloaded,
            ]
        )
        self.conn.commit()

    def get(self, app_name: str, version: int) -> typing.Optional[ApplicationVersion]:
        cur = self.conn.cursor()
        res = cur.execute(SELECT_QUERY, [app_name, version]).fetchone()
        if res is None:
            return None
        return _deserialize_application_version(res)

    def update(self, app_version: ApplicationVersion):
        cur = self.conn.cursor()
        cur.execute(
            UPDATE_QUERY,
            [
                app_version.installed_at.timestamp().__int__(),
                app_version.commit,
                app_version.path.resolve().__str__(),
                app_version.is_downloaded,
                app_version.app_name,
                app_version.version,
            ],
        )
        self.conn.commit()

    def list(self) -> typing.List[ApplicationVersion]:
        cur = self.conn.cursor()
        res = cur.execute(SELECT_ALL_QUERY).fetchall()
        repositories: typing.List[ApplicationVersion] = []
        for row in res:
            repositories.append(_deserialize_application_version(row))
        return repositories

    def remove(self, app_name: str, version: int) -> bool:
        cur = self.conn.cursor()
        cur.execute(DELETE_QUERY, [app_name, version])
        self.conn.commit()
        return cur.rowcount >= 1
