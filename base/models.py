from django.db import models
# from django.contrib.auth.models import AbstractUser


class Student(models.Model):
    studentId = models.CharField(max_length=10, unique=True)
    studentName = models.CharField(max_length=100)
    password = models.CharField(max_length=128)

    def __str__(self) -> str:
        return self.studentName
    
class Lecturer(models.Model):
    lecturerId = models.CharField(max_length=10, unique=True)
    lecturerName = models.CharField(max_length=100)
    password = models.CharField(max_length=128)

    def __str__(self) -> str:
        return self.lecturerName

# class Course(models.Model):
#     name = models.CharField(max_length=255)
#     # Add any other fields related to the course

# class EnrolledCourse(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)

# class ClassAttendance(models.Model):
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     unique_code = models.CharField(max_length=10)  # Assuming a unique code length of 10 characters
#     present_students = models.ManyToManyField(User, blank=True, related_name='attended_classes')