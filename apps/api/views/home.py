from core.common.service_code import ServiceCode
from core.lib.view import BaseView
from core.lib.route import Route
from apps.scheduler.app import add


@Route.route(path='api/home/')
class Home(BaseView):
    @Route.route(path='index')
    def index(self):
        a = add.delay(1, 2)
        return self.success({'sum': 1})

    @Route.route(path='home/1')
    def home(self):
        return self.failure(ServiceCode.param_not_exists, {'a': 1})

    @Route.route(path='home')
    def home1(self):
        return self.response(self.request_param)
