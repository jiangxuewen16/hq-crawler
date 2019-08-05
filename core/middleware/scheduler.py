from django.utils.deprecation import MiddlewareMixin


class Scheduler(MiddlewareMixin):

    def process_request(self, request):
        print(request)

    def process_response(self, request, response):
        return response
