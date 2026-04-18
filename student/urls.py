from django.urls import path , include
from . import views

urlpatterns = [
    path('dashboard/',views.student_dashboard , name="student_dashboard"),
    path('attendance/',views.student_attendance , name="student_attendance"),
    path('leave-request/', views.request_leave, name='request_leave'),
    path('results/', views.student_results, name='student_results'),
]