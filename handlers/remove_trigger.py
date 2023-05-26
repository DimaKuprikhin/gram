import typing

from context import Context


APP_NOT_FOUND_MESSAGE = (
'The application "{}" is not found. Use "gram add" command.'
)
INCORRECT_TRIGGER_TYPE_MESSAGE = (
'Incorrect trigger type. Use one of "always", "commit" and "timer".'
)


def handle(app_name: str, trigger_type: typing.Optional[str], context: Context):
    app = context.db.applications.get(app_name)
    if app is None:
        print(APP_NOT_FOUND_MESSAGE.format(app_name))
        return

    if trigger_type is None:
        context.db.triggers.remove(app_name)
    else:
        if trigger_type not in ['always', 'commit', 'timer']:
            print(INCORRECT_TRIGGER_TYPE_MESSAGE)
            return
        context.db.triggers.remove_by_type(app_name, trigger_type)
