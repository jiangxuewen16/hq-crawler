from django_apscheduler.jobstores import register_job

from apps.monitor.service import exception_service, rabbitmq_service
from core.lib.task import scheduler

"""
异常定时发送消息
"""


# @register_job(scheduler, "interval", seconds=10 * 60)
# def exception_send_email():
#     exception_service.send_email()
#
#
# @register_job(scheduler, "interval", seconds=10 * 60)
# def monitor_send_email():
#     rabbitmq_service.send_email()
