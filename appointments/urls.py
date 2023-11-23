from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('appointment/', views.appointment_list, name='appointment_list'),
    path('book-appointment', views.appointment_create, name='appointment_create'),
    path('<int:pk>/edit', views.appointment_edit, name='appointment_edit'),
    # path('<int:pk>/delete', views.appointment_delete, name='appointment_delete'),
    path('<int:pk>/approved', views.approve_appointment, name='approve_appointment'),
    path('<int:pk>/completed', views.complete_appointment, name='complete_appointment'),

    path('appointment-info', views.appointment_info, name='appointment_info'),

]