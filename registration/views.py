from django.http import HttpResponse


def home(request):
    return HttpResponse("New Group Student Registration Django project is running.")
