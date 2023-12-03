from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('report', views.report, name='report'),
    path('appointment report', views.appointment_report, name='appointment_report'),
    path('patient list report', views.patient_list_report, name='patient_list_report'),
    path('treatment list report', views.treatment_list_report, name='treatment_list_report'),

]
