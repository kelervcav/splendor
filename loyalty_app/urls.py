from django.urls import path
from . import views

app_name = 'loyalty'

urlpatterns = [
    path('home', views.home, name='home'),
    # login logout
    path('', views.process_login, name='loyalty_login'),
    path('logout/', views.process_logout, name='loyalty_logout'),

]