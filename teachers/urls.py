from django.urls import path
from . import views

urlpatterns = [
    # namespace teacher-specific routes under /teacher/
    path('teacher/dashboard/', views.teacher_dashboard, name="teacher_dashboard"),
    path('teacher/attendance/', views.take_attendance, name="take_attendance"),
    path('teacher/leave-requests/', views.leave_requests, name='leave_requests'),
    path('teacher/leave-requests/<int:pk>/reject/', views.reject_leave, name='reject_leave'),
    path('teacher/leave-approve/<int:pk>/', views.approve_leave, name='approve_leave'),
]
