import crontab

from context import Context


def handle(enable: bool, context: Context):
    cron = crontab.CronTab(user='dima')
    job = next(cron.find_command('/usr/local/bin/gram update > /home/dima/gram_log.txt'), None)
    if job is None:
        job = cron.new(user='dima', command='/usr/local/bin/gram update > /home/dima/gram_log.txt')
        job.setall('* * * * *')
    job.user = 'dima'
    job.enable(enable)
    cron.write(user='dima')
