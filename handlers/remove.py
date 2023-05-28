from context import Context
import utils


APP_NOT_FOUND_MESSAGE = (
'The application "{}" is not found. Use "gram add" command.'
)


def handle(app_name: str, context: Context):
    app = context.db.applications.get(app_name)
    if app is None:
        print(APP_NOT_FOUND_MESSAGE.format(app_name))
        return
    
    script = context.db.scripts.get(app_name)
    context.db.scripts.remove(app_name)
    context.db.triggers.remove(app_name)
    context.db.application_versions.remove(app_name)
    context.db.applications.remove(app_name)
    if script is not None:
        script.path.unlink()
    repos_dir = context.repos_dir / app_name
    utils.rmdir(repos_dir)
