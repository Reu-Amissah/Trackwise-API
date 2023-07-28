from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
from . import views

urlpatterns = [
    path('', views.endpoints),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('student', views.student)
    # path('lecturer', views.Lecturer)
]