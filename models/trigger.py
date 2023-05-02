import datetime
import typing


class IncorrectTriggerType(Exception):
    def __init__(self):
        pass


class Trigger:
    app_name: str
    type: str
    value: typing.Optional[str]
    currently_at: typing.Optional[str]

    def __init__(
        self,
        app_name: str,
        type: str,
        value: str = None,
        currently_at: str = None
    ):
        if type not in ['always', 'commit', 'timer']:
            raise IncorrectTriggerType()
        self.app_name = app_name
        self.type = type
        self.value = value
        self.currently_at = (
            currently_at if currently_at else datetime.datetime.utcnow()
        )
