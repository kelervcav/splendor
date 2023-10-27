from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    path('<int:pk>/add-points', views.create_transaction, name='create_transaction')
]