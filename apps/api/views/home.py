from django.http import FileResponse

from core.common.helper import get_scrapyd_cli
from core.lib.view import BaseView
from core.lib.route import Route


@Route.route(path='api/home/')
class Home(BaseView):
    @Route.route(path='index')
    def index(self):
        # a = add.delay()
        file = open('README.md', 'rb')
        print(type(file))
        return self.file_response(file)

    @Route.route(path='home/1')
    def home(self):
        # crawler.spot_comment()

        jobid = get_scrapyd_cli().schedule('spiders', 'ctrip_comment')
        print('=' * 30, '爬虫定时任务:::', '景区评论:::', ':::', jobid)
        jobid = get_scrapyd_cli().schedule('spiders', 'lvmama_comment')
        print('=' * 30, '爬虫定时任务:::', '景区评论:::', ':::', jobid)
        jobid = get_scrapyd_cli().schedule('spiders', 'mafengwo_comment')
        print('=' * 30, '爬虫定时任务:::', '景区评论:::', ':::', jobid)
        jobid = get_scrapyd_cli().schedule('spiders', 'meituan_comment')
        print('=' * 30, '爬虫定时任务:::', '景区评论:::', ':::', jobid)
        jobid = get_scrapyd_cli().schedule('spiders', 'fliggy_comment')
        print('=' * 30, '爬虫定时任务:::', '景区评论:::', ':::', jobid)
        jobid = get_scrapyd_cli().schedule('spiders', 'qunar_comment')
        print('=' * 30, '爬虫定时任务:::', '景区评论:::', ':::', jobid)
        jobid = get_scrapyd_cli().schedule('spiders', 'ly_comment')
        print('=' * 30, '爬虫定时任务:::', '景区评论:::', ':::', jobid)
        return self.success({})

    @Route.route(path='home')
    def home1(self):
        return self.response(self.request_param)
