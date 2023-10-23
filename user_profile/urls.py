from django.urls import path

from .views import ProfileListView
from . import views

app_name = 'users'

urlpatterns = [
    path('', ProfileListView.as_view(template_name='user_list.html'), name='list'),
    path('create/', views.profile_create, name='create'),
    path('<int:pk>/edit/', views.profile_edit, name='edit'),
    path('<int:pk>/disable/', views.profile_disable, name='disable'),

    path('group/list/', views.group_list, name='group_list'),
    path('group/create/', views.group_create, name='group_create'),
    path('group/<int:pk>/create/', views.group_edit, name='group_edit'),

    path('patient/', views.patient_list, name='patient_list'),
]
