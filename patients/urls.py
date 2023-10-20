from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    path('', views.home, name='home'),


    # patient
    path('create/', views.patient_create, name='patient_create'),

]
