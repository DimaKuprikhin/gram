import pathlib
import typing

from executer import Executer
from models.script import Script
from shell import Shell
import utils


INTRO = (
'''Execute necessary commands to install the application.
When everything is done, enter exit.
'''
)


class Installer:
    def install(self, app_name: str, dir: pathlib.PosixPath) -> typing.List[str]:
        shell = Shell(INTRO, app_name, Executer(dir))
        shell.cmdloop()
        history = shell.history
        history.append('')
        return history

    def update(self, script: Script, dir: pathlib.PosixPath):
        cmds: typing.List[str] = []
        with open(script.path, 'r') as f:
            cmds = f.read().split('\n')

        executer = Executer(dir)
        calls = utils.parse_script(cmds, {'cd': executer.cd, 'exit': None}, executer.execute)
        for handler, arg in calls:
            if handler is None:
                break
            handler(arg)
