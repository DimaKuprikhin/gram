import datetime

from context import Context


APP_NOT_FOUND_MESSAGE = (
'The application "{}" is not found. Use "gram add" command.'
)
MISSING_SCRIPT_MESSAGE = (
'''WARNING: The application "{}" hasn't been installed yet.
    Use command gram install to install it.'''
)


def handle(app_name: str, version: int, context: Context):
    app = context.db.applications.get(app_name)
    if app is None:
        print(APP_NOT_FOUND_MESSAGE.format(app_name))
        return
    
    script = context.db.scripts.get(app_name)
    if script is None:
        print(MISSING_SCRIPT_MESSAGE.format(app_name))
        return

    app_version = context.db.application_versions.get(app_name, version)
    if not app_version.is_downloaded:
        app_version.path.mkdir(parents=True)
        context.github.download(
            app.repo_owner, app.repo_name, app_version.commit, app_version.path,
        )
        app_version.is_downloaded = True

    context.installer.update(script, app_version.path)

    app_version.installed_at = datetime.datetime.utcnow()
    context.db.application_versions.update(app_version)
    app.current_version = version
    context.db.applications.update(app)
