from django.urls import path
from . import views

app_name = 'report_analytics'

urlpatterns = [
    path('treatment analytics', views.treatment_analytics, name='treatment_analytics'),
]
