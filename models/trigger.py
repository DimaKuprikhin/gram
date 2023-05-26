import datetime
import typing


class IncorrectTriggerType(Exception):
    def __init__(self):
        pass


class Trigger:
    app_name: str
    type: str
    update_period: typing.Optional[datetime.timedelta]

    def __init__(
        self,
        app_name: str,
        type: str,
        update_period: datetime.timedelta = None,
    ):
        if type not in ['always', 'commit', 'timer']:
            raise IncorrectTriggerType()
        self.app_name = app_name
        self.type = type
        self.update_period = update_period
