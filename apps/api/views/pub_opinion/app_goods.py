from scrapy import Request

from core.lib.route import Route
from core.lib.view import BaseView

@Route.route(path='api/ApplicationCenter/apporder')
class PublicOpinion(BaseView):

    @Route.route(path='/login')
    def login(self):
        login_url = r'http://11.75.1.29:8018/api/account/login'
        yield Request(url=login_url,  dont_filter=True, meta={'userName': 'admin', 'password': '1q2w3E*'})
