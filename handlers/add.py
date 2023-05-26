import typing

from context import Context
from github_client import RepositoryNotFound
from models.application import Application
import utils


EXISTING_APP_MESSAGE = (
    'The application "{}" is already added.'
)
NOT_EXISTING_REPO_MESSAGE = (
    'The repository with url "{}" doesn\'t exist.'
)


def handle(app_name: str, url: str, branch: typing.Optional[str], context: Context):
    if context.db.applications.get(app_name) is not None:
        print(EXISTING_APP_MESSAGE.format(app_name))
        return

    owner, name = utils.parse_github_url(url)
    try:
        default_branch = context.github.get_default_branch(owner, name)
    except RepositoryNotFound:
        print(NOT_EXISTING_REPO_MESSAGE.format(url))
    if not default_branch:
        default_branch = 'master'

    app = Application(
        app_name=app_name,
        current_version=0,
        repo_owner=owner,
        repo_name=name,
        branch=branch if branch else default_branch,
    )
    context.db.applications.add(app)
