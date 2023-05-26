import datetime
import typing

from context import Context
from models.application_version import ApplicationVersion
from models.application import Application
from models.trigger import Trigger
import utils


NO_APPS_MESSAGE = (
'No applications has been added. Use "gram add" command.'
)
APP_NOT_FOUND_MESSAGE = (
'The application "{}" is not found. Use "gram add" command.'
)
CHECK_APP_FOR_UPDATES_MESSAGE = (
'Check application "{}" for updates...'
)
UPDATING_APP_MESSAGE = (
'Performing update for application "{}"...'
)
SUCCESSFULL_UPDATE_MESSAGE = (
'The application "{}" was successfully updated.'
)
MISSING_SCRIPT_MESSAGE = (
'''WARNING: The application "{}" hasn't been installed yet.
    Use command gram install to install it.'''
)
NO_UPDATES_MESSAGE = (
'''No updates for application "{}".'''
)


def check_triggers(
        triggers: typing.List[Trigger],
        app: Application,
        app_version: ApplicationVersion,
        context: Context,
) -> bool:
    for trigger in triggers:
        if trigger.type == 'always':
            return True
        commit = context.github.get_current_commit(
                app.repo_owner,
                app.repo_name,
                app.branch
        )
        if app_version.commit == commit:
            return False
        if trigger.type == 'commit':
            return True
        if trigger.type == 'timer':
            now = datetime.datetime.utcnow()
            return (app_version.installed_at + trigger.update_period) <= now


def handle(app_name: typing.Optional[str], context: Context):
    apps = []
    if app_name is None:
        apps = context.db.applications.list()
        if len(apps) == 0:
            print(NO_APPS_MESSAGE)
            return
    else:
        apps.append(context.db.applications.get(app_name))
        if apps[0] is None:
            print(APP_NOT_FOUND_MESSAGE.format(app_name))
            return

    for app in apps:
        script = context.db.scripts.get(app.app_name)
        if script is None:
            print(MISSING_SCRIPT_MESSAGE.format(app.app_name))
            return
        print(CHECK_APP_FOR_UPDATES_MESSAGE.format(app.app_name))

        app_version = context.db.application_versions.get(
            app.app_name, app.current_version,
        )
        triggers = context.db.triggers.get(app.app_name)
        if check_triggers(triggers, app, app_version, context):
            print(UPDATING_APP_MESSAGE.format(app.app_name))

            version = app.current_version + 1
            path = context.repos_dir / app.app_name / f'v{version}'
            path.mkdir()
            commit = context.github.get_current_commit(
                app.repo_owner, app.repo_name, app.branch,
            )
            context.github.download(app.repo_owner, app.repo_name, commit, path)

            context.installer.update(script, path)

            app_version = ApplicationVersion(
                app_name=app.app_name,
                version=version,
                installed_at=datetime.datetime.utcnow(),
                commit=commit,
                path=path,
                is_downloaded=True,
            )
            context.db.application_versions.add(app_version)
            app.current_version = version
            context.db.applications.update(app)

            for v in range(1, version - context.config.versions_cached + 1):
                cached_version = context.db.application_versions.get(app.app_name, v)
                if cached_version is None or not cached_version.is_downloaded:
                    continue
                utils.rmdir(cached_version.path)
                cached_version.is_downloaded = False
                context.db.application_versions.update(cached_version)

            print(SUCCESSFULL_UPDATE_MESSAGE.format(app.app_name))
        else:
            print(NO_UPDATES_MESSAGE.format(app.app_name))
