import crontab
import getpass

from context import Context


def handle(enable: bool, context: Context):
    user = getpass.getuser()
    cron = crontab.CronTab(user=user)
    job = next(cron.find_command('/usr/local/bin/gram update'), None)
    if job is None:
        job = cron.new(user=user, command='/usr/local/bin/gram update')
        job.setall('* * * * *')
    job.enable(enable)
    cron.write(user=user)
