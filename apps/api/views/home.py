from django.http import FileResponse

from apps.scheduler.task import crawler
from core.common.service_code import ServiceCode
from core.lib.view import BaseView
from core.lib.route import Route
from apps.scheduler.app import add


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
        crawler.spot_comment()
        return self.success({})

    @Route.route(path='home')
    def home1(self):
        return self.response(self.request_param)
