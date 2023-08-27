from django.contrib import admin
from .models import Student, Lecturer, Course, User, ClassSession 
# Register your models here.

admin.site.register(User)
admin.site.register(Student)
admin.site.register(Lecturer)
admin.site.register(Course)
admin.site.register(ClassSession)
