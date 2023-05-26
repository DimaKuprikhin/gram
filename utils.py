import pathlib
import typing


class GithubUrlParsingException(Exception):
    pass


def rmdir(path: pathlib.PosixPath) -> bool:
    if not path.exists() or not path.is_dir():
        return False
    for item in path.iterdir():
        if item.is_dir():
            rmdir(item)
        else:
            item.unlink()
    path.rmdir()
    return True


def parse_github_url(url: str) -> typing.Tuple[str, str]:
    if not url.startswith('https://'):
        raise GithubUrlParsingException()
    url = url[8:]
    parts = url.split('/')
    if len(parts) != 3:
        raise GithubUrlParsingException()
    return parts[1], parts[2]

def make_github_url(owner: str, name: str, branch: str = None) -> str:
    url = f'https://github.com/{owner}/{name}'
    if branch is not None:
        url += f'/tree/{branch}'
    return url


def parse_script(
        cmds: typing.List[str],
        progs_map: typing.Dict[str, typing.Callable],
        default: typing.Callable
) -> typing.List[typing.Tuple[typing.Callable, str]]:
    result: typing.List[typing.Tuple[typing.Callable, str]] = []
    for cmd in cmds:
        parts = cmd.split(' ', maxsplit=1)
        prog = parts[0]
        arg = parts[1] if len(parts) == 2 else ''
        if prog in progs_map:
            result.append((progs_map[prog], arg))
        else:
            result.append((default, cmd))
    return result
