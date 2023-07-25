from django.urls import path
from . import views

urlpatterns = [
    path('', views.endpoints),
    path('user', views.users)
]