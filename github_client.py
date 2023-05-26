import json
import pathlib
import requests
import shutil
import typing
import zipfile

import utils


class RepositoryNotFound(Exception):
    pass


class GithubClient:
    def __init__(self, token: str):
        self.token = token

    def get_default_branch(self, owner: str, name: str) -> typing.Optional[str]:
        response = requests.api.get(
            url=f'https://api.github.com/repos/{owner}/{name}',
            headers={
                    'Accept': 'application/vnd.github+json',
                    'X-GitHub-Api-Version': '2022-11-28',
                    'Authorization': f'Bearer {self.token}',
            },
        )
        if response.status_code == 404:
            raise RepositoryNotFound()
        body = response.json()
        if 'default_branch' not in body:
            return None
        return body['default_branch']

    def download(self, owner: str, name: str, ref: str, dir: pathlib.PosixPath):
        response = requests.api.get(
            url=f'https://api.github.com/repos/{owner}/{name}/zipball/{ref}',
            headers={
                    'Accept': 'application/vnd.github+json',
                    'X-GitHub-Api-Version': '2022-11-28',
                    'Authorization': f'Bearer {self.token}',
            },
            allow_redirects=True,
        )
        zip_filepath = pathlib.PosixPath(f'/tmp/{owner}_{name}.zip')
        with open(zip_filepath, 'wb') as f:
            f.write(response.content)
        with zipfile.ZipFile(zip_filepath, 'r') as z:
            z.extractall(dir)
        subdir = dir.iterdir().__next__()
        shutil.copytree(subdir, dir, dirs_exist_ok=True)
        utils.rmdir(subdir)
        zip_filepath.unlink()

    def get_current_commit(self, owner: str, name: str, branch: str) -> str:
        response = requests.api.get(
                url=f'https://api.github.com/repos/{owner}/{name}/branches/{branch}',
                headers={
                    'Accept': 'application/vnd.github+json',
                    'X-GitHub-Api-Version': '2022-11-28',
                },
            )
        if response.status_code != 200:
            raise Exception(response.content.decode('utf-8'))
        return json.loads(response.content.decode('utf-8'))['commit']['sha']
