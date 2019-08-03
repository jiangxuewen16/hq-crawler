from django.http import HttpResponse


# Create your views here.
def index(request):
    print(request.get_full_path())
    return HttpResponse('success')

