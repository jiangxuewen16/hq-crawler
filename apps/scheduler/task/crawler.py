from django_apscheduler.jobstores import register_job

from core.common.helper import get_scrapyd_cli
from core.lib.task import scheduler

"""
设置定时任务，选择方式为interval，时间间隔为10s
另一种方式为每天固定时间执行任务，对应代码为：
@register_job(scheduler, 'cron', day_of_week='mon-fri', hour='9', minute='30', second='10',id='task_time')
"""


@register_job(scheduler, "cron", hour='16', minute='52', id='spot_info')
def spot_info():
    jobid = get_scrapyd_cli().schedule('spiders', 'ctrip_spot')
    print('='*30, '爬虫定时任务:::', '景区信息:::', jobid)
    jobid = get_scrapyd_cli().schedule('spiders', 'lvmama_spot')
    print('='*30, '爬虫定时任务:::', '景区信息:::', jobid)
    jobid = get_scrapyd_cli().schedule('spiders', 'mafengwo_spot')
    print('='*30, '爬虫定时任务:::', '景区信息:::', jobid)
    jobid = get_scrapyd_cli().schedule('spiders', 'meituan_spot')
    print('='*30, '爬虫定时任务:::', '景区信息:::', jobid)


@register_job(scheduler, "cron", hour='2', minute='10', id='spot_comment')
def spot_comment():
    jobid = get_scrapyd_cli().schedule('spiders', 'ctrip_spot')
    print('=' * 30, '爬虫定时任务:::', '景区信息:::', jobid)
    jobid = get_scrapyd_cli().schedule('spiders', 'lvmama_spot')
    print('=' * 30, '爬虫定时任务:::', '景区信息:::', jobid)
    jobid = get_scrapyd_cli().schedule('spiders', 'mafengwo_spot')
    print('=' * 30, '爬虫定时任务:::', '景区信息:::', jobid)
    jobid = get_scrapyd_cli().schedule('spiders', 'meituan_spot')
    print('=' * 30, '爬虫定时任务:::', '景区信息:::', jobid)

#
# @register_job(scheduler, "interval", seconds=4)
# def spot_in_meituan():
#     pass


