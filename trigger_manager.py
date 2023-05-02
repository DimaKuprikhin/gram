import pathlib
import typing
import sqlite3

from databases.triggers_db import TriggersDB
from models.trigger import Trigger


class UniqueTriggerException(Exception):
    def __init__(self):
        pass


class TriggerManager:
    db: TriggersDB
    dir: pathlib.PosixPath

    def __init__(self, dir: pathlib.PosixPath):
        self.dir = dir.resolve()
        if not self.dir.exists():
            self.dir.mkdir(parents=True)
        self._init_db()

    def _init_db(self):
        self.db = TriggersDB(self.dir / 'triggers.db')
        if not self.db.is_initialized():
            self.db.initialize()

    def add(self, app_name: str, trigger_type: str, value: typing.Optional[str]):
        trigger = Trigger(app_name, trigger_type, value, '')
        try:
            self.db.add(trigger)
        except sqlite3.IntegrityError:
            raise UniqueTriggerException()

    def get(self, app_name: str)-> typing.List[Trigger]:
        return self.db.get(app_name)

    def check(self, app_name: str)-> bool:
        triggers = self.db.get(app_name)
        for trigger in triggers:
            if trigger.type == 'always':
                return True
        return False

    def remove(self, app_name: str)-> bool:
        return self.db.remove(app_name)
