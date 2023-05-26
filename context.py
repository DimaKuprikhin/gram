import configparser
import pathlib

from databases.applications_db import ApplicationsDB
from databases.application_versions_db import ApplicationVersionsDB
from databases.scripts_db import ScriptsDB
from databases.triggers_db import TriggersDB
from github_client import GithubClient
from installer import Installer


DIR = pathlib.PosixPath.home() / '.gram'
DEFAULT_CONFIG = {
    'github_token': '',
    'versions_cached': 2,
}


class Config:
    github_token: str
    versions_cached: int

    def __init__(self):
        path = DIR / 'config.ini'
        if not path.exists():
            config = configparser.ConfigParser()
            config['Settings'] = DEFAULT_CONFIG
            with open(path, 'x') as f:
                config.write(f)
        config = configparser.ConfigParser()
        config.read(path)
        self.github_token = config['Settings']['github_token']
        self.versions_cached = int(config['Settings']['versions_cached'])
        if self.versions_cached < 1:
            self.versions_cached = 1


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
    config: Config
    db: Databases
    github: GithubClient
    installer: Installer
    repos_dir: pathlib.PosixPath
    scirpts_dir: pathlib.PosixPath

    def __init__(self):
        DIR.mkdir(exist_ok=True)
        self.config = Config()
        self.db = Databases(DIR)
        self.github = GithubClient(self.config.github_token)
        self.installer = Installer()
        self.repos_dir = DIR / 'repos'
        self.scirpts_dir = DIR / 'scripts'
        self.repos_dir.mkdir(parents=True, exist_ok=True)
        self.scirpts_dir.mkdir(parents=True, exist_ok=True)
