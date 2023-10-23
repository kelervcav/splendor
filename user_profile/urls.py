from django.urls import path

# from .views import ProfileListView
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.profile_list, name='list'),
    path('create/', views.profile_create, name='create'),
    path('<int:pk>/edit/', views.profile_edit, name='edit'),
    path('<int:pk>/disable/', views.profile_disable, name='disable'),

    path('group/list/', views.group_list, name='group_list'),
    path('group/create/', views.group_create, name='group_create'),
    path('group/<int:pk>/create/', views.group_edit, name='group_edit'),

    path('patient/', views.patient_list, name='patient_list'),

    path('<int:pk>/edit/password/', views.admin_edit_password,
         name='admin_password_update'),

    path('profile/edit/password/', views.profile_edit_password,
         name='own_profile_edit_password'),
]
