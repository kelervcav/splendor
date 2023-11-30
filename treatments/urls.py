from django.urls import path
from . import views

app_name = 'treatments'

urlpatterns = [
    # treatments
    path('', views.service_list, name='service_list'),
    path('create/', views.service_create, name='service_create'),
    path('<int:pk>/edit', views.service_edit, name='service_edit'),
    path('<int:pk>/disable', views.service_disable, name='service_disable'),

    path('service-list', views.services_list_loyalty, name='services_list_loyalty'),

    # treatment
    path('treatment/', views.treatment_list, name='treatment_list'),
    path('treatment/create/', views.treatment_create, name='treatment_create'),
    path('treatment/<int:pk>/edit', views.treatment_edit, name='treatment_edit'),
    path('treatment/<int:pk>/disable', views.treatment_disable, name='treatment_disable'),
]