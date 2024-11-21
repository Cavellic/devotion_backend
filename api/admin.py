from django.contrib import admin
from .models import Student, Devotion,StudentProfile, Attendance
# Register your models here.

admin.site.register(Student)
admin.site.register(Devotion)
admin.site.register(Attendance)
admin.site.register(StudentProfile)