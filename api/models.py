from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Student(models.Model):
    student_id = models.CharField(max_length = 100, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length = 255)
    program = models.CharField(max_length = 100)
    
    def __str__(self):
        return self.first_name

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='profile')
    
    def __str__(self):
        return str(self.student)

    
class Devotion(models.Model):
    date = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{self.title} on {self.date}"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True)
    devotion = models.ForeignKey(Devotion, on_delete=models.CASCADE)
    attended_at = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.first_name} attended {self.devotion.title} on {str(self.devotion.date)}"
    