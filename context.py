import pathlib

from databases.applications_db import ApplicationsDB
from databases.application_versions_db import ApplicationVersionsDB
from databases.scripts_db import ScriptsDB
from databases.triggers_db import TriggersDB
from github_client import GithubClient
from installer import Installer


DIR = pathlib.PosixPath.home() / '.gram'


class Databases:
    applications: ApplicationsDB
    application_versions: ApplicationVersionsDB
    scripts: ScriptsDB
    triggers: TriggersDB

    def __init__(self, dir: pathlib.PosixPath):
        self.applications = ApplicationsDB(dir / 'applications.sqlite')
        self.application_versions = ApplicationVersionsDB(
            dir / 'application_versions.sqlite'
        )
        self.scripts = ScriptsDB(dir / 'scripts.sqlite')
        self.triggers = TriggersDB(dir / 'triggers.sqlite')


class Context:
    db: Databases
    github: GithubClient
    installer: Installer
    repos_dir: pathlib.PosixPath
    scirpts_dir: pathlib.PosixPath

    def __init__(self, token: str):
        DIR.mkdir(exist_ok=True)
        self.db = Databases(DIR)
        self.github = GithubClient(token)
        self.installer = Installer()
        self.repos_dir = DIR / 'repos'
        self.scirpts_dir = DIR / 'scripts'
        self.repos_dir.mkdir(parents=True, exist_ok=True)
        self.scirpts_dir.mkdir(parents=True, exist_ok=True)
