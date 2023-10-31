from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='main'),
    path('<int:pk>/approved', views.approve_appointment_dashboard, name='approve_appointment_dashboard'),
]
