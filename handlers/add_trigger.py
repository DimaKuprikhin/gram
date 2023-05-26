import datetime
import typing

from context import Context
from models.trigger import Trigger


APP_NOT_FOUND_MESSAGE = (
'The application "{}" is not found. Use "gram add" command.'
)
EXISTING_TRIGGER_MESSAGE = (
'The application "{}" is already has trigger with type "{}".'
)


# 1d6h
def parse_update_period(s: str) -> datetime.timedelta:
    separators = [
        {
            'symbol': 'd',
            'value': datetime.timedelta(days=1),
        },
        {
            'symbol': 'h',
            'value': datetime.timedelta(hours=1),
        },
        {
            'symbol': 'm',
            'value': datetime.timedelta(minutes=1),
        },
        {
            'symbol': 's',
            'value': datetime.timedelta(seconds=1),
        },
    ]
    res = datetime.timedelta()
    for separator in separators:
        if separator['symbol'] in s:
            index = s.find(separator['symbol'])
            number = int(s[:index])
            res += number * separator['value']
            s = s[index+1:]
    return res


def handle(
        app_name: str,
        trigger_type: str,
        update_period: typing.Optional[str],
        context: Context
):
    app = context.db.applications.get(app_name)
    if app is None:
        print(APP_NOT_FOUND_MESSAGE.format(app_name))
        return

    trigger = context.db.triggers.get_by_type(app_name, trigger_type)
    if trigger is not None:
        print(EXISTING_TRIGGER_MESSAGE.format(app_name, trigger_type))
        return

    update_period_td = None
    if update_period:
        update_period_td = parse_update_period(update_period)
    trigger = Trigger(app_name, trigger_type, update_period_td)
    context.db.triggers.add(trigger)
