from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    path('', views.home, name='home'),

    # patient
    path('create/', views.patient_create, name='patient_create'),
    path('<int:pk>/edit/', views.patient_edit, name='patient_edit'),
    path('<int:pk>/disable/', views.patient_disable, name='patient_disable'),


]
