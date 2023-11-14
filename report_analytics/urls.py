from django.urls import path
from . import views

app_name = 'report_analytics'

urlpatterns = [
    path('report-analytics', views.report_analytics, name='report_analytics'),
]
