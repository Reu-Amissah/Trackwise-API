# from django.shortcuts import render
# from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Student
from .serializers import StudentSerializer
# Create your views here.

@api_view(['GET'])
def endpoints(request):
    data = ['/students', '/advocates/:usernamex']
    return Response(data)


@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
def student(request): 
    if request.method == 'GET':
        student = Student.objects.all()
        serializer = StudentSerializer(student, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        student = Student.objects.create(
            studentId = request.data['studentId'],
            studentName = request.data['studentName'],
            password = request.data['password']
        )
        serializer = StudentSerializer(student, many=False)

        return Response(serializer.data)