import cmd
import pathlib
import typing

from executer import Executer, ExecuterException


class Shell(cmd.Cmd):
    history: typing.List[str] = []
    executer: Executer

    def __init__(self, intro: str, prompt: str, executer: Executer):
        cmd.Cmd.__init__(self)
        self.intro = intro
        self.basic_prompt = prompt
        self.executer = executer
        self._update_prompt()

    def _update_prompt(self):
        dir = self.executer.dir
        home = pathlib.PosixPath.home()
        if dir == home:
            self.prompt = f'{self.basic_prompt}:~$ '
        elif dir.is_relative_to(home):
            path = dir.relative_to(home)
            self.prompt = f'{self.basic_prompt}:~/{path}$ '
        else:
            self.prompt = f'{self.basic_prompt}:{dir}$ '

    def default(self, cmd: str):
        self.history.append(cmd)
        stdout, stderr = self.executer.execute(cmd)
        if stdout:
            print(stdout, end='')
        if stderr:
            print(stderr, end='')

    def do_cd(self, arg: str):
        self.history.append(f'cd {arg}')
        try:
            self.executer.cd(arg)
        except ExecuterException as ex:
            print(ex)
        self._update_prompt()

    def do_exit(self, arg: str):
        return True
