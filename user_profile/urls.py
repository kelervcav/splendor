from django.urls import path

from .views import ProfileListView
from . import views

app_name = 'users'

urlpatterns = [
    path('', ProfileListView.as_view(template_name='user_list.html'), name='list'),
    path('create/', views.profile_create, name='create')
]