from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    indexNumber = models.CharField(max_length=10, unique=True)
    isStudent = models.BooleanField(default=True)


    def __str__(self) -> str:
        return self.username + " " + str(self.indexNumber)
    
#add token to each user
@receiver(post_save, sender=User)
def create_user_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.get_or_create(user=instance)

# for user in User.objects.all():
#     Token.objects.get_or_create(user=user)

class Course(models.Model):
    courseCode = models.CharField(max_length=10, unique=True)
    courseTitle = models.CharField(max_length=300)

    def __str__(self) -> str:
        return self.courseTitle

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    courses = models.ManyToManyField(Course, verbose_name="courses registered")

    def __str__(self) -> str:
        return self.user.username
    

class Lecturer(models.Model):
    lecturer = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    courses = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return self.lecturer.username
    
class ClassSession(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE, null=True)
    presentStudents = models.ManyToManyField(Student, verbose_name="students present", related_name="present_students", blank=True)
    absentStudents = models.ManyToManyField(Student, verbose_name="students absent", related_name="absent_students", blank=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.course.courseTitle + ": " + str(self.start_time) + " - " + str(self.end_time)