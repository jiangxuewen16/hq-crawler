from scrapyd_api import ScrapydAPI

from core.lib.route import Route
from core.lib.view import BaseView
from hq_crawler import settings


@Route.route(path='api/scrapy/')
class Scrapy(BaseView):
    """
    获取scrapyd api客户端
    """

    @classmethod
    def get_scrapyd_cli(cls) -> ScrapydAPI:
        return ScrapydAPI(settings.SCRAPYD_URL)

    @Route.route(path='list')
    def list(self):
        return self.success({'sd': self.get_scrapyd_cli().list_projects()})

    @Route.route(path='schedule')
    def schedule(self):
        return self.success({'sd': self.get_scrapyd_cli().schedule('hq_spider', 'hq')})
