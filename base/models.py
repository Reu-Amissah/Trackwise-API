from django.db import models
from django.contrib import auth
import uuid


class User(auth.models.User):
    indexNumber = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    isStudent = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.username + " " + str(self.indexNumber)
    
class Course(models.Model):
    courseCode = models.CharField(max_length=10, unique=True)
    courseTitle = models.CharField(max_length=300)

    def __str__(self) -> str:
        return self.courseTitle

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    courses = models.ManyToManyField(Course, verbose_name="courses registered")

    def __str__(self) -> str:
        return self.studentName
    

class Lecturer(models.Model):
    lecturer = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    courses = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return self.lecturerName
    
class ClassSession(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE, null=True)
    present_students = models.ManyToManyField(Student, verbose_name="students present", blank=True)
    absent_students = models.ManyToManyField(Student, verbose_name="students absent", blank=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.course.courseTitle + ": " + str(self.start_time) + " - " + str(self.end_time)