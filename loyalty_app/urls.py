from django.urls import path
from . import views

app_name = 'loyalty'

urlpatterns = [
    path('home', views.home, name='home'),
    path('list', views.service_list, name='service_list'),

]