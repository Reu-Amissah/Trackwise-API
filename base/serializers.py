from rest_framework.serializers import ModelSerializer
from .models import *

class UserSerializer(ModelSerializer):
    class Meta: 
        model = User
        fields = '__all__'


class CourseSerializer(ModelSerializer):
    class Meta: 
        model = Course
        fields = '__all__'

class StudentSerializer(ModelSerializer):
    student = UserSerializer()
    courses = CourseSerializer(many=True)
    class Meta: 
        model = Student
        fields = '__all__'

class LecturerSerializer(ModelSerializer):
    lecturer = UserSerializer()
    courses = CourseSerializer(many=True)
    class Meta: 
        model = Lecturer
        fields = '__all__'

class SessionSerializer(ModelSerializer):
    course = CourseSerializer()
    lecturer = LecturerSerializer()
    present_students = StudentSerializer(many=True)
    absent_students = StudentSerializer(many=True)
    class Meta: 
        model = ClassSession
        fields = '__all__'  