# from django.shortcuts import render
# from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer
# Create your views here.

@api_view(['GET'])
def endpoints(request):
    data = ['/advocates', '/advocates/:usernamex']
    return Response(data)


@api_view(['GET', 'POST'])
def users(request): 
    if request.method == 'GET':
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        user = User.objects.create(
            studentId = request.data['studentId'],
            studentName = request.data['studentName'],
            password = request.data['password']
        )
        serializer = UserSerializer(user, many=False)

        return Response(serializer.data)