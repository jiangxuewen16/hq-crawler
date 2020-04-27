from django.utils.deprecation import MiddlewareMixin

from core.lib.view import BaseView


class MiddleSetMethod(MiddlewareMixin):

    def process_request(self, request):
        BaseView.method = request.method

    def process_response(self, request, response):
        return response  # 执行完了这个中间件一定要 传递给下一个中间件

    def process_exception(self, request, exception):
        print('MiddleSetMethod的process_exception')
