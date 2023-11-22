from django.urls import path
from . import views

app_name = 'loyalty'

urlpatterns = [
    path('home', views.home, name='home'),
]