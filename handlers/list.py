import tabulate

from context import Context
import utils


def handle(context: Context):
    apps = context.db.applications.list()
    rows = []
    for app in apps:
        triggers = ' '.join([t.type for t in context.db.triggers.get(app.app_name)])
        if not triggers:
            triggers = '-'
        url = utils.make_github_url(app.repo_owner, app.repo_name, app.branch)
        version = str(app.current_version) if app.current_version > 0 else '-'
        row = [app.app_name, version, triggers, url]
        rows.append(row)
    print(tabulate.tabulate(rows, headers=['Application', 'Version', 'Triggers', 'URL']))
