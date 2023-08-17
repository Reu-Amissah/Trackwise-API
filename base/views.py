# from django.shortcuts import render
# from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from .models import *
from .serializers import *
from datetime import datetime


class UserAPIView(APIView):

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=201)
        return Response(serializer.errors, status=400)
    
    def put(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User updated successfully"}, status=201)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, pk):
        user = User.objects.get(pk=pk)
        user.delete()
        return Response({"message": "User deleted successfully"}, status=204)


class StudentAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk=None):
        if pk == "self":
            student = Student.objects.get(user=request.user)
            serializer = StudentSerializer(student)
        else:
            students = Student.objects.all()
            serializer = StudentSerializer(students, many=True)
        
        return Response(serializer.data, status=200)
    

class LecturerAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk=None):
        if pk == "self":
            lecturer = Lecturer.objects.get(lecturer=request.user)
            serializer = LecturerSerializer(lecturer)
        else:
            lecturers = Lecturer.objects.all()
            serializer = LecturerSerializer(lecturers, many=True)
        
        return Response(serializer.data, status=200)
    

class CourseAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if request.user.isStudent:
            student = Student.objects.get(user=request.user)
            courses = student.courses.all()
            serializer = CourseSerializer(courses, many=True)
        elif request.user.is_staff:
            lecturer = Lecturer.objects.get(lecturer=request.user)
            courses = lecturer.courses.all()
            serializer = CourseSerializer(courses, many=True)
        
        return Response(serializer.data, status=200)
    
    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Course created successfully"}, status=201)
        return Response(serializer.errors, status=400)
    
    def put(self, request, pk):
        course = Course.objects.get(pk=pk)
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Course updated successfully"}, status=201)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, pk):
        course = Course.objects.get(pk=pk)
        course.delete()
        return Response({"message": "Course deleted successfully"}, status=204)
    


class SessionAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get(self, request):
        if request.user.isStudent:
            student = Student.objects.get(user=request.user)
            sessions = ClassSession.objects.filter(course__in=student.courses.all())
            serializer = SessionSerializer(sessions, many=True)
        elif request.user.is_staff:
            lecturer = Lecturer.objects.get(lecturer=request.user)
            sessions = ClassSession.objects.filter(lecturer=lecturer)
            serializer = SessionSerializer(sessions, many=True)
        
        return Response(serializer.data, status=200)
    
    def post(self, request):
        data = request.data
        course = Course.objects.get(courseCode=data["course"])

        session = ClassSession.objects.create(
            course=course,
            lecturer=Lecturer.objects.get(lecturer=request.user)
        )
    
    def put(self, request, pk):
        session_id = request.data["session_id"]
        class_session = ClassSession.objects.get(pk=session_id)

        course = class_session.course
        if pk == "end-session":
            class_session.end_time = datetime.now()

            #record absent students
            registered_students = Student.objects.filter(courses__in=[course])
            present_students = class_session.present_students.all()
            class_session.absent_students = registered_students.exclude(pk__in=present_students)
            class_session.save()

        if pk == "restart-session":
            class_session.end_time = None
            class_session.save()

        if pk == "mark-present":
            student = Student.objects.get(user = request.user)
            class_session.present_students.add(student)
            class_session.save()

        return Response({"message": "Session updated successfully"}, status=201)
    
    def delete(self, request, pk):
        session = ClassSession.objects.get(pk=pk)
        session.delete()
        return Response({"message": "Session deleted successfully"}, status=204)

