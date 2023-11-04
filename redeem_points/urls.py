from django.urls import path
from . import views

app_name = 'redeem_points'

urlpatterns = [
   path('<int:pk>/redeem points', views.redeem_points, name='redeem_points'),

]
