import pathlib
import subprocess
import typing


class ExecuterException(Exception):
    pass


class Executer:
    dir: pathlib.PosixPath

    def __init__(self, dir: pathlib.PosixPath):
        self.dir = dir.resolve()

    def cd(self, dir: typing.Optional[str]):
        if not dir:
            self.dir = pathlib.PosixPath.home()
            return
        if len(dir.split(' ')) > 1:
            raise ExecuterException('cd: too many arguments')

        new_dir = self.dir / dir

        if not new_dir.exists():
            raise ExecuterException(f'cd: {dir}: No such file or directory')
        if not new_dir.is_dir():
            raise ExecuterException(f'cd: {dir}: Not a directory')
        self.dir = new_dir.resolve()

    def execute(self, cmd: str) -> typing.Tuple[str, str]:
        r = subprocess.run(cmd, shell=True, capture_output=True, cwd=self.dir)
        return r.stdout.decode(), r.stderr.decode()
