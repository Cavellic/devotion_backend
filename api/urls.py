from django.urls import path
from . import views

urlpatterns = [
    path('students/', views.StudentAPIView.as_view(), name='student-list-create'),
    path('students/<int:pk>/', views.StudentAPIView.as_view(), name='student-detail-delete'),
    path('devotions/', views.DevotionAPIView.as_view(), name='devotion-list-create'),
    path('devotions/<int:pk>/', views.DevotionAPIView.as_view(), name='devotion-detail'),
    path('attendances/', views.AttendanceAPIView.as_view(), name='attendance-list-create'),
    path('attendances/<int:pk>/', views.AttendanceAPIView.as_view(), name='attendance-detail'),
    path('add-attendance/', views.AddAttendanceView.as_view(), name='add_attendance'),
    path('devotions/today/', views.TodayDevotionListView.as_view(), name='today_devotion_list'),
    path('devotions/create/', views.DevotionCreateView.as_view(), name='create_devotion'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('user/', views.GetLoggedInUserView.as_view(), name='get_logged_in_user'),
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('attended-devotions/', views.AttendedDevotionsView.as_view(), name='attended-devotions'),
    path('register/', views.StudentRegistrationView.as_view(), name='student_register'),
]
