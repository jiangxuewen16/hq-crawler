from core.common.helper import get_scrapyd_cli
from core.lib.route import Route
from core.lib.view import BaseView
from django.utils.autoreload import logger


@Route.route(path='api/scrapy/')
class Scrapy(BaseView):

    @Route.route(path='list')
    def list(self):
        return self.success({'sd': get_scrapyd_cli().list_projects()})

    @Route.route(path='schedule')
    def schedule(self):
        return self.success({'sd': get_scrapyd_cli().schedule('spiders', 'mafengwo_spot')})

    @Route.route(path='del/project')
    def del_project(self):
        return self.success({'sd': get_scrapyd_cli().delete_project('spiders')})

    @Route.route(path='spot/info')
    def spot_info(self):
        jobid = get_scrapyd_cli().schedule('spiders', 'ctrip_spot')
        logger.info('=' * 30, '爬虫任务:::', '景区信息:::', ':::', jobid)
        jobid = get_scrapyd_cli().schedule('spiders', 'lvmama_spot')
        logger.info('=' * 30, '爬虫任务:::', '景区信息:::', ':::', jobid)
        jobid = get_scrapyd_cli().schedule('spiders', 'mafengwo_spot')
        logger.info('=' * 30, '爬虫任务:::', '景区信息:::', ':::', jobid)
        jobid = get_scrapyd_cli().schedule('spiders', 'meituan_spot')
        logger.info('=' * 30, '爬虫任务:::', '景区信息:::', ':::', jobid)
        return self.success({'jobid': jobid})

    @Route.route(path='spot/comment')
    def spot_comment(self):
        jobid = get_scrapyd_cli().schedule('spiders', 'ctrip_comment')
        logger.info('=' * 30, '爬虫任务:::', '景区携程评论:::', ':::', jobid)
        jobid = get_scrapyd_cli().schedule('spiders', 'lvmama_comment')
        logger.info('=' * 30, '爬虫任务:::', '景区驴妈妈评论:::', ':::', jobid)
        # jobid = get_scrapyd_cli().schedule('spiders', 'mafengwo_comment')
        # logger.info('=' * 30, '爬虫任务:::', '景区评论:::', ':::', jobid)
        jobid = get_scrapyd_cli().schedule('spiders', 'meituan_comment')
        logger.info('=' * 30, '爬虫任务:::', '景区美团评论:::', ':::', jobid)
        # jobid = get_scrapyd_cli().schedule('spiders', 'fliggy_comment')
        # logger.info('=' * 30, '爬虫任务:::', '景区评论:::', ':::', jobid)
        jobid = get_scrapyd_cli().schedule('spiders', 'comment_and_tag')
        logger.info('=' * 30, '爬虫任务:::', '景区去哪评论:::', ':::', jobid)
        jobid = get_scrapyd_cli().schedule('spiders', 'ly_comment')
        logger.info('=' * 30, '爬虫任务:::', '景区同程评论:::', ':::', jobid)
        return self.success({'jobid': jobid})

    @Route.route(path='spot/list/meituan')
    def spot_list_(self):
        jobid = get_scrapyd_cli().schedule('spiders', 'meituan_city_spot')
        logger.info('=' * 30, '爬虫定时任务:::', '美团景区列表:::', ':::', jobid)
        return self.success({'jobid': jobid})

    @Route.route(path='spot/list/ctrip')
    def spot_list_(self):
        jobid = get_scrapyd_cli().schedule('spiders', 'ctrip_city_spot')
        logger.info('=' * 30, '爬虫定时任务:::', '美团景区列表:::', ':::', jobid)
        return self.success({'jobid': jobid})

    @Route.route(path='spot/list/qunar')
    def spot_list_(self):
        jobid = get_scrapyd_cli().schedule('spiders', 'qunar_comment')
        logger.info('=' * 30, '爬虫定时任务:::', '去哪儿列表:::', ':::', jobid)
        return self.success({'jobid': jobid})

    @Route.route(path='hqlx/order')
    def hqlx_order_(self):
        jobid = get_scrapyd_cli().schedule('spiders', 'hqlx_order')
        logger.info('=' * 30, 'test:::test', jobid)
        return self.success({'jobid': jobid})
