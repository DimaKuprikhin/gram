import cmd
import pathlib
import typing

from executer import Executer, ExecuterException


class AbortException(Exception):
    pass


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

    def _do_cd(self, arg: str):
        try:
            self.executer.cd(arg)
        except ExecuterException as ex:
            print(ex)
        self._update_prompt()

    def default(self, cmd: str):
        if cmd.startswith('@'):
            cmd = cmd[1:].lstrip()
            if cmd.startswith('cd'):
                cmd = cmd[2:].lstrip()
                self._do_cd(cmd)
                return
        else:
            self.history.append(cmd)
        stdout, stderr = self.executer.execute(cmd)
        if stdout:
            print(stdout, end='')
        if stderr:
            print(stderr, end='')

    def do_cd(self, arg: str):
        self.history.append(f'cd {arg}')
        self._do_cd(arg)

    def do_commit(self, arg: str):
        return True

    def do_abort(self, arg: str):
        raise AbortException()
