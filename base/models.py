from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
#import set_password
from django.contrib.auth.hashers import make_password


class User(AbstractUser):
    indexNumber = models.CharField(max_length=10, unique=True)
    isStudent = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'indexNumber'

    def save(self, *args, **kwargs):
        if self.isStudent:
            self.is_staff = False
        else:
            self.is_staff = True
        self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)


    def __str__(self) -> str:
        return self.username + " " + str(self.indexNumber)
    
#add token to each user
@receiver(post_save, sender=User)
def create_user_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.get_or_create(user=instance)


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
    session_key = models.CharField(max_length=100, unique=True, blank=True, null=True)
    presentStudents = models.ManyToManyField(Student, verbose_name="students present", related_name="present_students", blank=True)
    absentStudents = models.ManyToManyField(Student, verbose_name="students absent", related_name="absent_students", blank=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        #generate session key
        key = uuid.uuid4()
        self.session_key = key
        super(ClassSession, self).save(*args, **kwargs)


    def __str__(self) -> str:
        return self.course.courseTitle + ": " + str(self.start_time) + " - " + str(self.end_time)