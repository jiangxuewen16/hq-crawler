from django_apscheduler.jobstores import register_job

from core.lib.task import scheduler


@register_job(scheduler, "interval", seconds=4)
def my_job():
    print('xxxxxxxxxxxxxxxxxx')
