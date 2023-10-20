from django.shortcuts import render
from treatments.models import Service


# Create your views here.
def home(request):
    return render(request,"loyalty/home.html")


def service_list(request):
    service_list = Service.objects.all()
    return render(request, 'treatments/service_list.html', {'service_list': service_list})
