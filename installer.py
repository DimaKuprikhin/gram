import pathlib

from databases.scripts_db import ScriptsDB
from shell import Shell


INTRO = (
'''Execute necessary commands to install the application.
When everything is done, enter exit.
'''
)


class ExistingScriptException(Exception):
    def __init__(self):
        super(Exception).__init__()


class IncorrectReinstallUsage(Exception):
    def __init__(self):
        super(Exception).__init__()


class Installer:
    db: ScriptsDB
    dir: pathlib.PosixPath
    scripts_dir: pathlib.PosixPath

    def __init__(self, dir: pathlib.PosixPath):
        self.dir = dir.resolve()
        if not self.dir.exists():
            self.dir.mkdir(parents=True)

        self.scripts_dir = self.dir / 'scripts'
        if not self.scripts_dir.exists():
            self.scripts_dir.mkdir()

        self._init_db()

    def _init_db(self):
        self.db = ScriptsDB(self.dir / 'scripts.db')
        if not self.db.is_initialized():
            self.db.initialize()

    def install(self, app_name: str, reinstall: bool, dir: pathlib.PosixPath):
        already_exists = self.db.get(app_name) is not None
        if already_exists and not reinstall:
            raise ExistingScriptException()
        if not already_exists and reinstall:
            raise IncorrectReinstallUsage()

        shell = Shell(INTRO, app_name, dir)
        shell.cmdloop()
        history = shell.history
        history.append('')

        script_path = self.scripts_dir / app_name
        if script_path.exists():
            script_path.unlink()
        with open(script_path, 'x') as f:
            f.write('\n'.join(shell.history))
        if not reinstall:
            self.db.add(app_name, script_path)
