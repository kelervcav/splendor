from django.urls import path

from .views import ProfileListView
from . import views

app_name = 'users'

urlpatterns = [
    path('', ProfileListView.as_view(template_name='user_list.html'), name='list'),
    path('create/', views.profile_create, name='create'),
    path('<int:pk>/dit/', views.profile_edit, name='edit'),
    path('<int:pk>/disable/', views.profile_disable, name='disable'),

    path('group/create/', views.group_create, name='group_create'),

    path('patient/', views.patient_list, name='patient_list'),
]
