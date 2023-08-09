from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('', views.endpoints),
    path('auth/login/', obtain_auth_token, name="login"),
    path('student', views.student)
    # path('lecturer', views.Lecturer)
]