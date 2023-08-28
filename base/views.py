# from django.shortcuts import render
# from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from .models import *
from .serializers import *
from datetime import datetime
from django.contrib.auth import authenticate


class LoginAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = (AllowAny,)

    def post(self, request):
        status = request.GET.get("status")

        username = request.data["username"]
        password = request.data["password"]

        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:

            token, _ = Token.objects.get_or_create(user=user)

            if status == "student":
                if user.isStudent:
                    return Response({"message": "Login successful", "token": token.key}, status=200)
                else:
                    return Response({"message": "Login failed"}, status=401)
            elif status == "lecturer":
                if user.is_staff:
                    return Response({"message": "Login successful", "token": token.key}, status=200)
                else:
                    return Response({"message": "Login failed"}, status=401)
            else:
                return Response({"message": "Login failed"}, status=401)
            
        return Response({"message": "Login failed"}, status=401)

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
        """
        /students/?courseCode=DCIT400

        reurns all students registered for a course
        """
        courseCode = request.GET.get("courseCode")
        if courseCode:
            course = Course.objects.get(courseCode=courseCode)
            students = Student.objects.filter(courses__in=[course])
            serializer = StudentSerializer(students, many=True)

            return Response(serializer.data, status=200)

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

    def get(self, request, pk=None):
        if request.user.isStudent:
            student = Student.objects.get(user=request.user)
            courses = student.courses.all()
            serializer = CourseSerializer(courses, many=True)

        elif request.user.is_staff:
            if pk:
                if pk == "details":
                    courseCode = request.GET.get("courseCode")
                    course = Course.objects.get(courseCode=courseCode)
                    students = Student.objects.filter(courses__in=[course])
                    course_serializer = CourseSerializer(course)
                    student_serializer = StudentSerializer(students, many=True)
                    return Response({"course": course_serializer.data, "students": student_serializer.data}, status=200)

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


    def get(self, request, pk=None):

        sessionKey = request.GET.get("sessionKey")
        courseCode = request.GET.get("courseCode")

        if request.user.isStudent:
            """
            /sessions/
            """
            student = Student.objects.get(user=request.user)
            sessions = ClassSession.objects.filter(course__in=student.courses.all())
            serializer = SessionSerializer(sessions, many=True)

        elif request.user.is_staff:
            """
            /sessions/all-sessions/?courseCode=DCIT400
            """
            if pk=="all-sessions":
                course = Course.objects.get(courseCode=courseCode)
                sessions = ClassSession.objects.filter(course__in=[course])
                serializer = SessionSerializer(sessions, many=True)
                return Response(serializer.data, status=200)
            '''
            /sessions/?sessionKey=123
            '''
            session = ClassSession.objects.get(pk=sessionKey)
            serializer = SessionSerializer(session)
        
        return Response(serializer.data, status=200)
    
    def post(self, request):
        if request.user.isStudent:
            return Response({"message": "Unauthorized"}, status=401)
        
        data = request.data
        course = Course.objects.get(courseCode=data["courseCode"])

        session = ClassSession.objects.create(
            course=course,
            lecturer=Lecturer.objects.get(lecturer=request.user)
        )

        key = session.session_key

        return Response({"message": "Session created successfully", "key": key}, status=201)
    
    def put(self, request, pk=None):
        sessionKey = request.GET.get("sessionKey")
        status = request.GET.get("status")

        class_session = ClassSession.objects.get(pk=sessionKey)

        """
        /sessions/?sessionKey=123&status=mark-present
        """
        course = class_session.course
        if status == "end-session":
            class_session.end_time = datetime.now()

            #record absent students
            registered_students = Student.objects.filter(courses__in=[course])
            present_students = class_session.presentStudents.all()
            class_session.absentStudents = registered_students.exclude(pk__in=present_students)
            class_session.save()

        if status == "restart-session":
            class_session.end_time = None
            class_session.save()

        if status == "mark-present":
            student = Student.objects.get(user = request.user)
            class_session.presentStudents.add(student)
            class_session.save()

        return Response({"message": "Session updated successfully"}, status=201)
    
    def delete(self, request, pk):
        session = ClassSession.objects.get(pk=pk)
        session.delete()
        return Response({"message": "Session deleted successfully"}, status=204)

