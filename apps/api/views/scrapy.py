from scrapyd_api import ScrapydAPI

from core.common.helper import get_scrapyd_cli
from core.lib.route import Route
from core.lib.view import BaseView
from hq_crawler import settings


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
