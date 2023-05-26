import typing

HELP_MESSAGE = (
'''Usage: gram command

Commands:
  add-trigger - Add update trigger for specific application
  add - Bind an application name to github repository
  install - Download repository and perform manual installation
  list - List added applications and its info
  remove-trigger - Remove update trigger for specific application
  remove - Remove application and all its data
  revert - Perform automatic installation of specific application version
  update-by-timer - Enable or disable cron job that performs automatic updates
  update - Perform automatic updates

"gram help command" shows help message for specific command
'''
)
ADD_TRIGGER_HELP = (
'''Usage: gram add-triger app-name trigger-type [update-period]

Adds a trigger for application automatic update.
"trigger-type" must be one of "always", "commit" or "timer".
"update-period" must be provided only for "timer" triggers with format "\d+d\d+h\d+m\d+s"

Examples:
  - gram add-trigger app commit
  - gram add-trigger app2 timer 5m
  - gram add-trigger app3 timer 1d12h
'''
)
ADD_HELP = (
'''Usage: gram add app-name url [branch]

Binds an application with name "app-name" to github repository with specific branch.
If branch is not provided, default one is used (master/main).

Examples:
  - gram add app https://github.com/GithubUserName/repository-name
  - gram add app2 https://github.com/GithubUserName/repository-name non-main-branch
'''
)
INSTALL_HELP = (
'''Usage: gram install app [--reinstall]

Downloads repository on current commit and runs manual installation process.
If an application already has installation script, --reinstall option must be provided.

Examples:
  - gram install app
  - gram install app2 --reinstall
'''
)
LIST_HELP = (
'''Usage: gram list

Lists all added applications and its info.
'''
)
REMOVE_TRIGGER_HELP = (
'''Usage: gram remove-trigger app-name [trigger-type]

Removes trigger with trigger-type for specific application.
If trigger-type is not provided, removes all triggers for an application.

Examples:
  - gram remove-trigger app
  - gram remove-trigger app2 timer
'''
)
REMOVE_HELP = (
'''Usage: gram remove app-name

Removes an application and all its data.
'''
)
REVERT_HELP = (
'''Usage: gram revert app-name version

Performs automatic installation of specified application with provided version.

Examples:
  - gram revert app 2
'''
)
UPDATE_BY_TIMER_HELP = (
'''Usage: gram update-by-timer value

Enables or disables cron job that performing automatic updates of applications.

Examples:
  - gram update-by-timer 0 // disables automatic updates
  - gram update-by-timer 1 // enables automatic updates
'''
)
UPDATE_HELP = (
'''Usage: gram update [app-name]

Performs automatic update for specific application based on its triggers.
If app-name if not provided, all added application is checked for updates.

Examples:
  - gram update
  - gram update app
'''
)


def handle(command: typing.Optional[str]):
    command_help = {
        'add-trigger': ADD_TRIGGER_HELP,
        'add': ADD_HELP,
        'install': INSTALL_HELP,
        'list': LIST_HELP,
        'remove-trigger': REMOVE_TRIGGER_HELP,
        'remove': REMOVE_HELP,
        'revert': REVERT_HELP,
        'update-by-timer': UPDATE_BY_TIMER_HELP,
        'update': UPDATE_HELP,
    }
    if command in command_help:
        print(command_help[command])
    else:
        print(HELP_MESSAGE)