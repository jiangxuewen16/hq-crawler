from django.utils.deprecation import MiddlewareMixin
from django.utils.autoreload import logger



class Scheduler(MiddlewareMixin):

    def process_request(self, request):
        pass
        # logger.info(request)

    def process_response(self, request, response):
        return response
