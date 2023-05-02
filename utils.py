import json
import pathlib
import requests
import typing


class GithubUrlParsingException(Exception):
    def __init__(self):
        super(Exception).__init__()


def download_repo(owner: str, name: str, path: pathlib.PosixPath):
    response = requests.api.get(
        url=f'https://api.github.com/repos/{owner}/{name}/contents',
        headers={
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28',
        },
    )
    if response.status_code != 200:
        raise response

    for item in json.loads(response.content.decode()):
        content = requests.api.get(
            url=item['download_url']
        ).content
        with open(path / item['path'], 'x') as f:
            f.write(content.decode('utf-8'))

def rmdir(path: pathlib.PosixPath)-> bool:
    if not path.exists() or not path.is_dir():
        return False
    for item in path.iterdir():
        if item.is_dir():
            rmdir(item)
        else:
            item.unlink()
    path.rmdir()
    return True

def parse_github_url(url: str)-> typing.Tuple[str, str]:
    if not url.startswith('https://'):
        raise GithubUrlParsingException()
    url = url[8:]
    parts = url.split('/')
    if len(parts) != 3:
        raise GithubUrlParsingException()
    return parts[1], parts[2]

def make_github_url(owner: str, name: str)-> str:
    return f'https://github.com/{owner}/{name}'
