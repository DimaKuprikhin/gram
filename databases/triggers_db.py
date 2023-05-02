import sqlite3
import pathlib
import typing

from models.trigger import Trigger


CHECK_TABLE_QUERY = (
    '''SELECT name FROM sqlite_master
    WHERE type=\'table\' AND name=\'triggers\';'''
)
CREATE_TABLE_QUERY = (
    '''CREATE TABLE triggers (
        app_name TEXT,
        type TEXT NOT NULL,
        value TEXT,
        currently_at TEXT,
        PRIMARY KEY (app_name, type)
    );'''
)
INSERT_QUERY = (
    '''INSERT INTO triggers (app_name, type, value, currently_at)
    VALUES (?, ?, ?, ?);'''
)
SELECT_QUERY = (
    '''SELECT app_name, type, value, currently_at
    FROM triggers
    WHERE app_name = ?;'''
)
SELECT_ALL_QUERY = (
    '''SELECT app_name, type, value, currently_at
    FROM triggers;'''
)
DELETE_QUERY = (
    '''DELETE FROM triggers
    WHERE app_name = ?;'''
)


class TriggersDB:
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

    def add(self, trigger: Trigger):
        cur = self.conn.cursor()
        cur.execute(
            INSERT_QUERY,
            [
                trigger.app_name,
                trigger.type,
                trigger.value,
                trigger.currently_at
            ]
        )
        self.conn.commit()

    def get(self, app_name: str) -> typing.List[Trigger]:
        cur = self.conn.cursor()
        res = cur.execute(SELECT_QUERY, [app_name]).fetchall()
        triggers: typing.List[Trigger] = []
        for row in res:
            triggers.append(Trigger(row[0], row[1], row[2], row[3]))
        return triggers

    def list(self) -> typing.List[Trigger]:
        cur = self.conn.cursor()
        res = cur.execute(SELECT_ALL_QUERY).fetchall()
        repositories: typing.List[Trigger] = []
        for row in res:
            repositories.append(Trigger(
                row[0], row[1], row[2], row[3]))
        return repositories

    def remove(self, app_name: str) -> bool:
        cur = self.conn.cursor()
        cur.execute(DELETE_QUERY, app_name)
        self.conn.commit()
        return cur.rowcount >= 1
