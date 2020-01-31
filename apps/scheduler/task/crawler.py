from django_apscheduler.jobstores import register_job

from core.common.helper import get_scrapyd_cli
from core.lib.task import scheduler
from apps.api.model.exception import ExcLog
from django.utils.autoreload import logger

"""
设置定时任务，选择方式为interval，时间间隔为10s
另一种方式为每天固定时间执行任务，对应代码为：
@register_job(scheduler, 'cron', day_of_week='mon-fri', hour='9', minute='30', second='10',id='task_time')
"""


# @register_job(scheduler, "cron", hour='02', minute='10', id='spot_info')
# def spot_info():
#     jobid = get_scrapyd_cli().schedule('spiders', 'ctrip_spot')
#     logger.info('=' * 30, '爬虫定时任务:::', '景区信息:::', jobid)
#     jobid = get_scrapyd_cli().schedule('spiders', 'lvmama_spot')
#     logger.info('=' * 30, '爬虫定时任务:::', '景区信息:::', jobid)
#     jobid = get_scrapyd_cli().schedule('spiders', 'mafengwo_spot')
#     logger.info('=' * 30, '爬虫定时任务:::', '景区信息:::', jobid)
#     jobid = get_scrapyd_cli().schedule('spiders', 'meituan_spot')
#     logger.info('=' * 30, '爬虫定时任务:::', '景区信息:::', jobid)


@register_job(scheduler, "cron", hour='02', minute='10', id='spot_comment')
def spot_comment():
    logger.info("==========【景区评论：开启】==========")
    jobid = get_scrapyd_cli().schedule('spiders', 'ctrip_comment')
    jobid = get_scrapyd_cli().schedule('spiders', 'lvmama_comment')
    jobid = get_scrapyd_cli().schedule('spiders', 'mafengwo_comment')
    jobid = get_scrapyd_cli().schedule('spiders', 'meituan_comment')
    jobid = get_scrapyd_cli().schedule('spiders', 'fliggy_comment')
    jobid = get_scrapyd_cli().schedule('spiders', 'qunar_comment')
    jobid = get_scrapyd_cli().schedule('spiders', 'ly_comment')
    logger.info("==========【景区评论：结束】==========")


@register_job(scheduler, "cron", hour='03', minute='10', id='spot_comment')
def spot_price():
    logger.info("==========【价格监控：开启】==========")
    jobid = get_scrapyd_cli().schedule('spiders', 'ctrip_price')
    jobid = get_scrapyd_cli().schedule('spiders', 'fliggy_spot')
    jobid = get_scrapyd_cli().schedule('spiders', 'lvmama_spot_price')
    jobid = get_scrapyd_cli().schedule('spiders', 'ly_price')
    jobid = get_scrapyd_cli().schedule('spiders', 'Mafengwo_price')
    jobid = get_scrapyd_cli().schedule('spiders', 'MeituanPrice')
    jobid = get_scrapyd_cli().schedule('spiders', 'qunar_price')
    logger.info("==========【价格监控：结束】==========")



# 订单接口检测 每2秒执行一次
# @register_job(scheduler, "interval", seconds=5 * 60 * 60)
# def order_check():
#     jobid = get_scrapyd_cli().schedule('spiders', 'hqlx_order')
#     logger.info('=' * 30, 'test:::', 'test:::', jobid)

@register_job(scheduler, "interval", seconds=5)
def order_check():
    logger.info('=' * 30 + "测试定时任务")
