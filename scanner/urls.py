from django.urls import path
from . import views

urlpatterns = [
    path('qr-code-scanner', views.scan_qrcode, name="scan_qrcode"),
]