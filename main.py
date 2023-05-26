#!/usr/bin/python3
import argparse

from context import Context
import handlers.add_trigger
import handlers.add
import handlers.install
import handlers.list
import handlers.update
import handlers.remove_trigger
import handlers.remove


context = Context('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')


def add(args):
    handlers.add.handle(args.app_name, args.url, args.branch, context)


def install(args):
    handlers.install.handle(args.app_name, args.reinstall, context)


def add_trigger(args):
    update_period = args.update_period if hasattr(
        args, 'update_period') else None
    handlers.add_trigger.handle(
        args.app_name, args.trigger_type, update_period, context,
    )


def remove_trigger(args):
    trigger_type = args.trigger_type if hasattr(args, 'trigger_type') else None
    handlers.remove_trigger.handle(args.app_name, trigger_type, context)


def remove(args):
    handlers.remove.handle(args.app_name, context)


def list(args):
    handlers.list.handle(context)


def update(args):
    handlers.update.handle(
        args.app_name if hasattr(args, 'app_name') else None,
        context
    )


parser = argparse.ArgumentParser(prog='gram')

sp = parser.add_subparsers(dest='command', required=True)

add_parser = sp.add_parser('add')
add_parser.add_argument('app_name', metavar='app-name', type=str)
add_parser.add_argument('url', type=str)
add_parser.add_argument('branch', type=str, default=None, nargs='?')
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
always_trigger_parser.set_defaults(func=add_trigger)

commit_trigger_parser = trigger_sp.add_parser('commit')
commit_trigger_parser.set_defaults(func=add_trigger)

timer_trigger_parser = trigger_sp.add_parser('timer')
timer_trigger_parser.add_argument('update_period', metavar='update-period', type=str)
timer_trigger_parser.set_defaults(func=add_trigger)

remove_trigger_parser = sp.add_parser('remove-trigger')
remove_trigger_parser.add_argument('app_name', metavar='app-name', type=str)
remove_trigger_parser.add_argument('trigger_type', metavar='trigger-type', type=str, nargs='?')
remove_trigger_parser.set_defaults(func=remove_trigger)

remove_parser = sp.add_parser('remove')
remove_parser.add_argument('app_name', metavar='app-name', type=str)
remove_parser.set_defaults(func=remove)

list_parser = sp.add_parser('list')
list_parser.set_defaults(func=list)

update_parser = sp.add_parser('update')
update_parser.add_argument('app_name', metavar='app-name', type=str, nargs='?')
update_parser.set_defaults(func=update)

args = parser.parse_args()
args.func(args)
