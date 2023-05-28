import datetime

from context import Context
from models.application_version import ApplicationVersion
from models.application import Application
from models.script import Script
from shell import AbortException
import utils


APP_NOT_FOUND_MESSAGE = (
'The application "{}" is not found. Use "gram add" command.'
)
EXISTING_SCRIPT_MESSAGE = (
'''The application "{}" is already has installation script.
Use option --reinstall to create new installation script.'''
)
INCORRECT_REINSTALL_MESSAGE = (
'Incorrect usage of --reinstall option: the application "{}" hasn\'t been installed yet.'
)


def install(app: Application, version: int, context: Context):
    app_name = app.app_name
    commit = context.github.get_current_commit(
        app.repo_owner, app.repo_name, app.branch
    )
    path = context.repos_dir / app_name / f'v{version}'
    path.mkdir(parents=True)
    # TODO: don't download if no new commits.
    context.github.download(app.repo_owner, app.repo_name, commit, path)

    try:
        history = context.installer.install(app_name, path)
    except AbortException as ex:
        utils.rmdir(path)
        return
    installed_at = datetime.datetime.utcnow()

    script = Script(app_name, context.scirpts_dir / app_name)
    if script.path.exists():
        script.path.unlink()
    with open(script.path, 'x') as f:
        f.write('\n'.join(history))
    if version == 1:
        context.db.scripts.add(script)

    app_version = ApplicationVersion(app_name, version, installed_at, commit, path, True)
    context.db.application_versions.add(app_version)
    app.current_version = version
    context.db.applications.update(app)

    for v in range(1, version - context.config.versions_cached + 1):
        cached_version = context.db.application_versions.get(app_name, v)
        if cached_version is None or not cached_version.is_downloaded:
            continue
        utils.rmdir(cached_version.path)
        cached_version.is_downloaded = False
        context.db.application_versions.update(cached_version)


def handle(app_name: str, reinstall: bool, context: Context):
    app = context.db.applications.get(app_name)
    if app is None:
        print(APP_NOT_FOUND_MESSAGE.format(app_name))
        return

    script = context.db.scripts.get(app_name)
    if script is None and reinstall:
        print(INCORRECT_REINSTALL_MESSAGE.format(app_name))
        return
    if script is not None and not reinstall:
        print(EXISTING_SCRIPT_MESSAGE.format(app_name))
        return

    if reinstall:
        install(app, app.current_version + 1, context)
    else:
        install(app, 1, context)
