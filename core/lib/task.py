from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events

from core.common import helper
from hq_crawler import settings

scheduler = BackgroundScheduler()
# 调度器使用DjangoJobStore()
scheduler.add_jobstore(DjangoJobStore(), "default")

"""
设置定时任务，选择方式为interval，时间间隔为10s
另一种方式为每天固定时间执行任务，对应代码为：
@register_job(scheduler, 'cron', day_of_week='mon-fri', hour='9', minute='30', second='10',id='task_time')
"""
helper.auto_import_module(settings.TASK_WORK_PACKAGE)

register_events(scheduler)
scheduler.start()
