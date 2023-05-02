import subprocess
import cmd
import pathlib
import typing


class Shell(cmd.Cmd):
    history: typing.List[str] = []

    def __init__(self, intro: str, prompt: str, dir: pathlib.PosixPath):
        cmd.Cmd.__init__(self)
        self.intro = intro
        self.basic_prompt = prompt
        self._set_dir(dir)

    def _set_dir(self, dir: pathlib.PosixPath):
        self.dir = dir.resolve()
        home = pathlib.PosixPath.home()
        if self.dir == home:
            self.prompt = f'{self.basic_prompt}:~$ '
        elif self.dir.is_relative_to(home):
            path = self.dir.relative_to(home)
            self.prompt = f'{self.basic_prompt}:~/{path}$ '
        else:
            self.prompt = f'{self.basic_prompt}:{self.dir}$ '

    def default(self, cmd: str):
        self.history.append(cmd)
        r = subprocess.run(cmd, shell=True, capture_output=True, cwd=self.dir.resolve())
        if r.stdout:
            print(r.stdout.decode())
        if r.stderr:
            print(r.stderr.decode())

    def do_cd(self, arg: str):
        self.history.append(f'cd {arg}')
        if not arg:
            self._set_dir(pathlib.PosixPath.home())
            return
        if len(arg.split(' ')) > 1:
            print('cd: too many arguments')
            return
        new_dir = self.dir / arg
        if not new_dir.exists():
            print(f'cd: {arg}: No such file or directory')
            return
        if not new_dir.is_dir():
            print(f'cd: {arg}: Not a directory')
            return
        self._set_dir(new_dir)

    def do_exit(self, arg: str):
        return True
