from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('auth/login/', views.LoginAPIView.as_view(), name="login"),
    
    path('users/', views.UserAPIView.as_view(), name='users'),
    path('users/<str:pk>/', views.UserAPIView.as_view(), name='user'),

    path('students/', views.StudentAPIView.as_view(), name='students'),
    path('students/<str:pk>/', views.StudentAPIView.as_view(), name='student'),

    path('lecturers/', views.LecturerAPIView.as_view(), name='lecturers'),
    path('lecturers/<str:pk>/', views.LecturerAPIView.as_view(), name='lecturer'),

    path('courses/', views.CourseAPIView.as_view(), name='courses'),
    path('courses/<str:pk>/', views.CourseAPIView.as_view(), name='course'),

    path('sessions/', views.SessionAPIView.as_view(), name='sessions'),
    path('sessions/<str:pk>/', views.SessionAPIView.as_view(), name='session'),

    path('edit_description/', views.EditDescriptionAPIView.as_view(), name='edit_description'),
]