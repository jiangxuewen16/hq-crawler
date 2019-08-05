import json

from django.http import HttpResponse
from django.views import View


class User(View):
    # Create your views here.
    def post(self, request):
        print(request)
        print(self.request)
        a = json.dumps({'name': 'jiangxuewen', 'age': 20})
        return HttpResponse(a, content_type="application/json")
