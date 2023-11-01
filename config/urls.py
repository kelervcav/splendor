"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views

from loyalty_app.views import process_login
from user_profile.views import process_admin_login

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('admin/', process_admin_login, name='login'),
    path('', process_login, name='loyalty_login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('/logout/', auth_views.LogoutView.as_view(next_page='loyalty_login'), name='loyalty_logout'),
    path('dashboard/', include('dashboard.urls'), name='dashboard'),
    path('users/', include('user_profile.urls'), name='users'),
    path('treatments/', include('treatments.urls'), name='treatments'),
    path('patients/', include('patients.urls'), name='patients'),
    path('appointments/', include('appointments.urls'), name='appointments'),
    path('loyalty/', include('loyalty_app.urls'), name='loyalty'),
    path('transactions/', include('transactions.urls'), name='transactions'),
    path('redemptions/', include('redemptions.urls'), name='redemptions'),
]
