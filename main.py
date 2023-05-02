#!/usr/bin/python3
import argparse
import pathlib

from installer import Installer, ExistingScriptException, IncorrectReinstallUsage
from repository_manager import RepositoryManager
from trigger_manager import TriggerManager, UniqueTriggerException


DIR = pathlib.PosixPath.home() / '.gram'


EXISTING_REPO_MESSAGE = (
'The application "{}" is already added.'
)
EXISTING_SCRIPT_MESSAGE = (
'''The application "{}" is already has installation script.
Use option --reinstall to create new installation script.'''
)
INCORRECT_REINSTALL_MESSAGE = (
'Incorrect usage of --reinstall option: the application "{}" hasn\'t been installed yet.'
)
APP_NOT_FOUND = (
'The application "{}" is not found.'
)
EXISTING_TRIGGER_MESSAGE = (
'The application "{}" is already has trigger with type "{}".'
)


def add(args):
    manager = RepositoryManager(DIR)
    if manager.get(args.app_name) is not None:
        print(EXISTING_REPO_MESSAGE.format(args.app_name))
        return
    manager.add(args.app_name, args.url)

def install(args):
    manager = RepositoryManager(DIR)
    repo = manager.get(args.app_name)
    installer = Installer(DIR)
    try:
        installer.install(repo.app_name, args.reinstall, repo.path)
    except ExistingScriptException:
        print(EXISTING_SCRIPT_MESSAGE.format(args.app_name))
    except IncorrectReinstallUsage:
        print(INCORRECT_REINSTALL_MESSAGE.format(args.app_name))

def add_always_trigger(args):
    repos_manager = RepositoryManager(DIR)
    if repos_manager.get(args.app_name) is None:
        print(APP_NOT_FOUND.format(args.app_name))
        return

    trigger_manager = TriggerManager(DIR)
    try:
        trigger_manager.add(args.app_name, args.trigger_type, None)
    except UniqueTriggerException:
        print(EXISTING_TRIGGER_MESSAGE.format(args.app_name, args.trigger_type))

parser = argparse.ArgumentParser(prog='gram')

sp = parser.add_subparsers(dest='command', required=True)

add_parser = sp.add_parser('add')
add_parser.add_argument('app_name', metavar='app-name', type=str)
add_parser.add_argument('url', type=str)
add_parser.set_defaults(func=add)

install_parser = sp.add_parser('install')
install_parser.add_argument('app_name', metavar='app-name', type=str)
install_parser.add_argument('--reinstall', action='store_true', default=False)
install_parser.set_defaults(func=install)

add_trigger_parser = sp.add_parser('add-trigger')
add_trigger_parser.add_argument('app_name', metavar='app-name', type=str)
trigger_sp = add_trigger_parser.add_subparsers(
    dest='trigger_type', metavar='trigger-type', required=True)

always_trigger_parser = trigger_sp.add_parser('always')
always_trigger_parser.set_defaults(func=add_always_trigger)

args = parser.parse_args()
args.func(args)
