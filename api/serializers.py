from rest_framework import serializers
from .models import Student, Devotion,StudentProfile, Attendance
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


# Serializer for User model (you can include fields as needed)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        
        
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                # Return both user and token for further processing
                data['user'] = user
                return data
            else:
                raise serializers.ValidationError("Invalid username or password.")
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")

    def save(self):
        user = self.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return token, user.is_superuser



class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'student_id', 'first_name', 'last_name', 'program']


class DevotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Devotion
        fields = ['id', 'date', 'title', 'description']
        
from rest_framework import serializers
from .models import Student, Devotion, Attendance

class AddAttendanceSerializer(serializers.Serializer):
    student_id = serializers.CharField(max_length=100)
    devotion_id = serializers.IntegerField()

    def validate(self, data):
        # Validate that the student exists
        try:
            data['student'] = Student.objects.get(student_id=data['student_id'])
        except Student.DoesNotExist:
            raise serializers.ValidationError({"student_id": "Student does not exist."})
        
        # Validate that the devotion exists
        try:
            data['devotion'] = Devotion.objects.get(id=data['devotion_id'])
        except Devotion.DoesNotExist:
            raise serializers.ValidationError({"devotion_id": "Devotion does not exist."})
        
        # Check if the attendance already exists
        if Attendance.objects.filter(student=data['student'], devotion=data['devotion']).exists():
            raise serializers.ValidationError("This student has already attended this devotion.")
        
        return data

    def create(self, validated_data):
        # Create the Attendance record
        attendance = Attendance.objects.create(
            student=validated_data['student'],
            devotion=validated_data['devotion']
        )
        return attendance

 
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_superuser']
        

class StudentProfileSerializer(serializers.ModelSerializer):
    student = StudentSerializer()

    class Meta:
        model = StudentProfile
        fields = ['user', 'student']
        
class AttendanceSerializer(serializers.ModelSerializer):
    student = StudentSerializer()  # Ensures nested data for Student
    devotion = DevotionSerializer()  # Ensures nested data for Devotion
    class Meta:
        model = Attendance
        fields = ['id', 'student', 'devotion', 'attended_at']
        
from rest_framework import serializers
from .models import Attendance

class AttendedDevotionSerializer(serializers.ModelSerializer):
    # Include nested devotion details
    title = serializers.CharField(source='devotion.title', read_only=True)
    description = serializers.CharField(source='devotion.description', read_only=True)
    date = serializers.DateField(source='devotion.date', read_only=True)

    class Meta:
        model = Attendance
        fields = ['date', 'title', 'description', 'attended_at']


from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Student, StudentProfile

class StudentRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, min_length=6)
    student_id = serializers.CharField(max_length=100)

    def validate_student_id(self, value):
        # Check if the student exists
        if not Student.objects.filter(student_id=value).exists():
            raise serializers.ValidationError("Student with this ID does not exist.")
        
        # Check if the student is already linked to a user profile
        if StudentProfile.objects.filter(student__student_id=value).exists():
            raise serializers.ValidationError("This student ID is already linked to a user.")
        return value

    def create(self, validated_data):
        # Create a new User
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )

        # Link the user to the StudentProfile
        student = Student.objects.get(student_id=validated_data['student_id'])
        StudentProfile.objects.create(user=user, student=student)

        return user


