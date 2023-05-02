import sqlite3
import pathlib
import typing


CHECK_TABLE_QUERY = (
    '''SELECT name FROM sqlite_master
    WHERE type=\'table\' AND name=\'scripts\';'''
)
CREATE_TABLE_QUERY = (
    '''CREATE TABLE scripts (
        app_name TEXT PRIMARY KEY,
        path TEXT
    );'''
)
INSERT_QUERY = (
    '''INSERT INTO scripts (app_name, path)
    VALUES (?, ?);'''
)
SELECT_QUERY = (
    '''SELECT path FROM scripts WHERE app_name = ?;'''
)
DELETE_QUERY = (
    '''DELETE FROM scripts WHERE app_name = ?;'''
)


class ScriptsDB:
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

    def add(self, app_name: str, path: pathlib.PosixPath):
        cur = self.conn.cursor()
        cur.execute(INSERT_QUERY, [app_name, str(path)])
        self.conn.commit()

    def get(self, app_name: str)-> typing.Optional[pathlib.PosixPath]:
        cur = self.conn.cursor()
        res = cur.execute(SELECT_QUERY, [app_name]).fetchone()
        if res is None:
            return None
        return pathlib.PosixPath(res[0])

    def remove(self, app_name: str)-> bool:
        cur = self.conn.cursor()
        res = cur.execute(DELETE_QUERY, [app_name])
        return res.rowcount >= 1
