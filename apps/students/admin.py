from django.contrib import admin
from apps.teachers.models import Teacher
from apps.students.models import Student, Assignment

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Assignment)