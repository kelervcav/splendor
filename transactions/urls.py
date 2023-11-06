from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    path('<int:pk>/add-points', views.transaction_create, name='transaction_create'),
    path('transaction-list', views.transaction_history, name='transaction_history'),

]
