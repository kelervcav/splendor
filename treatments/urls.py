from django.urls import path
from . import views

app_name = 'treatments'

urlpatterns = [
    # treatments
    path('', views.service_list, name='service_list'),
    path('create/', views.service_create, name='service_create'),
    path('<int:pk>/edit', views.service_edit, name='service_edit'),
    path('<int:pk>/disable', views.service_disable, name='service_disable'),

    # treatment area
    path('areas/', views.area_list, name='area_list'),
    path('area/create/', views.area_create, name='area_create'),
    path('area/<int:pk>/edit', views.area_edit, name='area_edit'),
    path('area/<int:pk>/disable', views.area_disable, name='area_disable'),

    # price type
    path('price-type/', views.price_type_list, name='price_type_list'),
    path('price-type/create/', views.price_type_create, name='price_type_create'),
    path('price-type/<int:pk>/edit', views.price_type_edit, name='price_type_edit'),
    path('price-type/<int:pk>/disable', views.price_type_disable, name='price_type_disable'),

    # treatment
    path('treatment/', views.treatment_list, name='treatment_list'),
    path('treatment/create/', views.treatment_create, name='treatment_create'),
    path('treatment/<int:pk>/edit', views.treatment_edit, name='treatment_edit'),
    path('treatment/<int:pk>/disable', views.treatment_disable, name='treatment_disable'),
]