# apicaller/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_view, name='api_view'),
]
