import datetime
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
        update_period INTEGER,
        PRIMARY KEY (app_name, type)
    );'''
)
INSERT_QUERY = (
    '''INSERT INTO triggers (
        app_name,
        type,
        update_period
    )
    VALUES (?, ?, ?);'''
)
SELECT_QUERY = (
    '''SELECT app_name, type, update_period
    FROM triggers
    WHERE app_name = ?;'''
)
SELECT_ALL_QUERY = (
    '''SELECT app_name, type, update_period
    FROM triggers;'''
)
DELETE_QUERY = (
    '''DELETE FROM triggers
    WHERE app_name = ? and type = ?;'''
)


def _deserialize_trigger(row) -> Trigger:
    return Trigger(
        row[0],
        row[1],
        datetime.timedelta(seconds=row[2]) if row[2] else None,
    )


class TriggersDB:
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


    def add(self, trigger: Trigger):
        cur = self.conn.cursor()
        cur.execute(
            INSERT_QUERY,
            [
                trigger.app_name,
                trigger.type,
                int(trigger.update_period.total_seconds())
                if trigger.update_period
                else None,
            ]
        )
        self.conn.commit()


    def get(self, app_name: str) -> typing.List[Trigger]:
        cur = self.conn.cursor()
        res = cur.execute(SELECT_QUERY, [app_name]).fetchall()
        triggers: typing.List[Trigger] = []
        for row in res:
            triggers.append(_deserialize_trigger(row))
        return triggers


    def get_by_type(self, app_name: str, type: str) -> typing.Optional[Trigger]:
        cur = self.conn.cursor()
        res = cur.execute(SELECT_QUERY, [app_name]).fetchall()
        res = [t for t in res if t[1] == type]
        assert len(res) <= 1
        return _deserialize_trigger(res[0]) if len(res) == 1 else None


    def list(self) -> typing.List[Trigger]:
        cur = self.conn.cursor()
        res = cur.execute(SELECT_ALL_QUERY).fetchall()
        repositories: typing.List[Trigger] = []
        for row in res:
            repositories.append(_deserialize_trigger(row))
        return repositories


    def remove(self, app_name: str, type: str) -> bool:
        cur = self.conn.cursor()
        cur.execute(DELETE_QUERY, [app_name, type])
        self.conn.commit()
        return cur.rowcount >= 1
