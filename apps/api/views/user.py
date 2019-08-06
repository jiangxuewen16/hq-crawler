from core.lib.view import BaseView
from core.lib.route import Route


@Route.route(path='api/user')
class User(BaseView):

    @Route.route(path='/user/index')
    def index(self):
        return self.response(self.requestParam)

    @Route.route(path='/user/home/1')
    def home(self):
        return self.response({'a': 2})

    @Route.route(path='/user/home/')
    def home1(self):
        return self.response(self.requestParam)
