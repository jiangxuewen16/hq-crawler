from django_apscheduler.jobstores import register_job

from core.lib.task import scheduler

"""
设置定时任务，选择方式为interval，时间间隔为10s
另一种方式为每天固定时间执行任务，对应代码为：
@register_job(scheduler, 'cron', day_of_week='mon-fri', hour='9', minute='30', second='10',id='task_time')
"""


@register_job(scheduler, "interval", seconds=1)
def my_job():
    print(11111111111)


@register_job(scheduler, "interval", seconds=2)
def my_job2():
    print(22222222222222)


@register_job(scheduler, "interval", seconds=4)
def my_job3():
    print(4444444444444)


