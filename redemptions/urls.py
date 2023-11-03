from django.urls import path
from . import views

app_name = 'redemptions'

urlpatterns = [
   path('<int:pk>/redeem points', views.redeem_points, name='redeem_points'),

]
