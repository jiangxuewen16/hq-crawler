from core.lib.route import Route
from core.lib.view import BaseView


@Route.route(path='api/task')
class Task(BaseView):
    @Route.route(path='/start')
    def start(self):
        pass
