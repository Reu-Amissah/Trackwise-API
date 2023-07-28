from django.contrib import admin
from .models import Student, Lecturer, Course
# Register your models here.


admin.site.register(Student)
admin.site.register(Lecturer)
admin.site.register(Course)