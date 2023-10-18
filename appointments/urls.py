from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('appointment/', views.appointment_list, name='appointment_list'),
    path('<int:pk>/edit', views.appointment_edit, name='appointment_edit'),
    path('<int:pk>/delete', views.appointment_delete, name='appointment_delete'),

]