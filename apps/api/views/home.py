from core.lib.base_view import BaseView
from core.lib.route import Route


@Route.route(path='api/home/')
class Home(BaseView):

    @Route.route(path='index')
    def index(self):
        return self.response(self.requestParam)

    @Route.route(path='home/1')
    def home(self):
        return self.response({'a': 1})

    @Route.route(path='home')
    def home1(self):
        return self.response(self.requestParam)
