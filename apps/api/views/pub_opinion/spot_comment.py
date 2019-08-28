from core.lib.view import BaseView
from core.lib.route import Route


@Route.route(path='api/spot/public/opinion')
class PublicOpinion(BaseView):

    @Route.route(path='/index')
    def index(self):

        return self.success(self.request_param)
