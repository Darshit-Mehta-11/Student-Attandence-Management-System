from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name="login"),
    path('register/', views.student_register, name='student_register'),
    path('teacher/', views.teacher_register, name='teacher_register'),
    path('logout/', views.logout, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
]
