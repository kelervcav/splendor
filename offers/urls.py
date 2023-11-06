from config.urls import path
from . import views


app_name = 'offers'

urlpatterns = [
    path('list', views.offer_list, name='offer_list'),
    path('create', views.offer_create, name='offer_create'),
    path('<int:pk>/edit', views.offer_edit, name='offer_edit'),
    path('<int:pk>/disable', views.offer_disable, name='offer_disable'),
    path('offer-list', views.offer_list_loyalty, name='offer_list_loyalty'),

]
