from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    path('', views.home, name='home'),
    path('book-appointment', views.appointment_create, name='appointment_create'),
    path('appointment-info', views.appointment_info, name='appointment_info'),

]
