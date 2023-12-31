from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [

    # patient
    path('list', views.patient_list, name='patient_list'),
    path('create/', views.patient_create, name='patient_create'),
    path('<int:pk>/edit/', views.patient_edit, name='patient_edit'),
    path('<int:pk>/disable/', views.patient_disable, name='patient_disable'),
    path('<int:pk>/patient-information', views.patient_info, name='patient_info'),
    path('<int:pk>/patient-renewal', views.patient_renewal, name='patient_renewal'),
    path('<int:pk>/patient-profile', views.patient_profile, name='patient_profile'),
    # reset password
    path('<int:pk>/reset/password/', views.reset_password, name='reset_password'),
    path('<int:pk>/generate-password/', views.generate_password, name='generate_password'),
    # change password for patient
    path('change password', views.change_password, name='change_password'),
    # scanner
    path('qr_scan', views.scanner, name='scanner'),
    # scanned patient information
    path('patient-information', views.scanned_patient_info, name='scanned_patient_info'),

]
