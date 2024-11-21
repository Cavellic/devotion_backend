from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Student, Devotion, Attendance
from .serializers import StudentSerializer,UserSerializer, DevotionSerializer,AttendanceSerializer, AddAttendanceSerializer,LoginSerializer
from django.utils import timezone
from rest_framework import generics
from rest_framework import status, permissions
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny


class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            token, is_superuser = serializer.save()
            return Response({"token": token.key, "is_superuser": is_superuser}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk=None):
        """Retrieve a single student if `pk` is provided, else list all students."""
        if pk:
            student = get_object_or_404(Student, pk=pk)
            serializer = StudentSerializer(student)
            return Response(serializer.data)
            print(request.user.username)
        else:
            students = Student.objects.all()
            serializer = StudentSerializer(students, many=True)
            return Response(serializer.data)

    def post(self, request):
        """Create a new student."""
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        """Delete a student by primary key (`pk`)."""
        student = get_object_or_404(Student, pk=pk)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DevotionAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk=None):
        if pk:
            devotion = get_object_or_404(Devotion, pk=pk)
            serializer = DevotionSerializer(devotion)
            print(request.user.username)
            return Response(serializer.data)
        else:
            devotions = Devotion.objects.all()
            serializer = DevotionSerializer(devotions, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = DevotionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AttendanceAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk=None):
        if pk:
            attendance = get_object_or_404(Attendance, pk=pk)
            serializer = AttendanceSerializer(attendance)
            return Response(serializer.data)
        else:
            attendance_records = Attendance.objects.all()
            serializer = AttendanceSerializer(attendance_records, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class TodayDevotionListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DevotionSerializer

    def get_queryset(self):
        today = timezone.now().date()
        return Devotion.objects.filter(date=today)
    
class DevotionCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Devotion.objects.all()
    serializer_class = DevotionSerializer
    

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AddAttendanceSerializer

class AddAttendanceView(APIView):
    def post(self, request):
        serializer = AddAttendanceSerializer(data=request.data)
        if serializer.is_valid():
            attendance = serializer.save()
            return Response({
                "success": f"{attendance.student.first_name} added to {attendance.devotion.title}."
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    
class GetLoggedInUserView(APIView):
    """
    View to return the logged-in user's data.
    Only authenticated users can access this view.
    """
    permission_classes = [IsAuthenticated]  # Ensures that the user is authenticated

    def get(self, request):
        """
        Retrieve the logged-in user's data.
        """
        # Access the logged-in user via request.user
        
        user = request.user

        # Serialize the user's data
        user_serializer = UserSerializer(user)

        # Return the serialized user data as the response
        return Response(user_serializer.data, status=status.HTTP_200_OK)
    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import StudentProfile
from .serializers import StudentProfileSerializer

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = StudentProfile.objects.get(user=request.user)
            serializer = StudentProfileSerializer(profile)
            return Response(serializer.data)
        except StudentProfile.DoesNotExist:
            return Response({"error": "Profile not found."}, status=404)
        
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Attendance, StudentProfile
from .serializers import AttendedDevotionSerializer

class AttendedDevotionsView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access

    def get(self, request):
        # Get the logged-in user's student profile
        student_profile = get_object_or_404(StudentProfile, user=request.user)
        student = student_profile.student

        # Retrieve the devotions the student has attended
        attended_devotions = Attendance.objects.filter(student=student).select_related('devotion')

        # Serialize the attendance records
        serializer = AttendedDevotionSerializer(attended_devotions, many=True)

        return Response(serializer.data)




class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Delete the user's token to log them out
        
        request.user.auth_token.delete()
        return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import StudentRegistrationSerializer

class StudentRegistrationView(APIView):
    def post(self, request):
        serializer = StudentRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "message": "Student registered successfully.",
                    "username": user.username
                },
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

