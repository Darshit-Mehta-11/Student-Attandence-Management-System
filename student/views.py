from django.shortcuts import render, redirect
from accounts.models import CustomUser
from teachers.models import Attendance, LeaveRequest
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LeaveRequestForm

# Create your views here.

def student_dashboard(request):
    if not request.user.is_authenticated or request.user.role != 'student':
        return redirect("login")
    
    username = request.user
    student = CustomUser.objects.get(username=username)
    # example timetable structure: days and periods
    # subjects and timetable based on student's stream
    stream = student.stream.lower() if student.stream else ''
    if stream == 'commerce':
        subjects = ['Accounting','Business Studies','Economics','Math','English']
        timetable = [
            {'day':'Monday','period1':'Accounting','period2':'Business Studies','period3':'Economics','period4':'Math'},
            {'day':'Tuesday','period1':'English','period2':'Accounting','period3':'Business Studies','period4':'Economics'},
            {'day':'Wednesday','period1':'Math','period2':'English','period3':'Accounting','period4':'Business Studies'},
            {'day':'Thursday','period1':'Economics','period2':'Math','period3':'English','period4':'Accounting'},
            {'day':'Friday','period1':'Business Studies','period2':'Economics','period3':'Math','period4':'English'},
        ]
    elif stream == 'science':
        subjects = ['Physics','Chemistry','Biology','Math','English']
        timetable = [
            {'day':'Monday','period1':'Physics','period2':'Chemistry','period3':'Biology','period4':'Math'},
            {'day':'Tuesday','period1':'English','period2':'Physics','period3':'Chemistry','period4':'Biology'},
            {'day':'Wednesday','period1':'Math','period2':'English','period3':'Physics','period4':'Chemistry'},
            {'day':'Thursday','period1':'Biology','period2':'Math','period3':'English','period4':'Physics'},
            {'day':'Friday','period1':'Chemistry','period2':'Biology','period3':'Math','period4':'English'},
        ]
    elif stream == 'arts':
        subjects = ['History','Geography','Political Science','Economics','English']
        timetable = [
            {'day':'Monday','period1':'History','period2':'Geography','period3':'Political Science','period4':'Economics'},
            {'day':'Tuesday','period1':'English','period2':'History','period3':'Geography','period4':'Political Science'},
            {'day':'Wednesday','period1':'Economics','period2':'English','period3':'History','period4':'Geography'},
            {'day':'Thursday','period1':'Political Science','period2':'Economics','period3':'English','period4':'History'},
            {'day':'Friday','period1':'Geography','period2':'Political Science','period3':'Economics','period4':'English'},
        ]
    else:
        subjects = ['Math', 'Physics', 'Chemistry', 'Biology', 'English']
        timetable = [
            {'day': 'Monday', 'period1': 'Math', 'period2': 'Physics', 'period3': 'Chemistry', 'period4': 'English'},
            {'day': 'Tuesday', 'period1': 'Biology', 'period2': 'Math', 'period3': 'History', 'period4': 'Computer'},
            {'day': 'Wednesday', 'period1': 'Physics', 'period2': 'Chemistry', 'period3': 'Math', 'period4': 'Physical Ed.'},
            {'day': 'Thursday', 'period1': 'English', 'period2': 'Biology', 'period3': 'Math', 'period4': 'Art'},
            {'day': 'Friday', 'period1': 'Computer', 'period2': 'History', 'period3': 'Physics', 'period4': 'Math'},
        ]
    # fetch notifications for this student
    from .models import Notification
    notifications = Notification.objects.filter(student=student)
    # if none exist, create a few sample notifications
    if not notifications.exists():
        msgs = [
            'Midterm exams begin next week.',
            'Library will be closed on Friday.',
            'New assignments available in Math.',
        ]
        for m in msgs:
            Notification.objects.create(student=student, message=m)
        notifications = Notification.objects.filter(student=student)
    return render(request, 'student/student_dashbord.html', {
        'student': student,
        'timetable': timetable,
        'subjects': subjects,
        'notifications': notifications,
    })


@login_required
def student_attendance(request):
    if not request.user.role == 'student':
        return redirect('login')
    username = request.user.username
    student = CustomUser.objects.get(username=username)
    records = Attendance.objects.filter(student=student).order_by('-semester','-date')

    return render(request, 'student/view_attendance.html', {"student":student,'records': records})

@login_required
def student_results(request):
    if request.user.role != 'student':
        return redirect('login')
    student = request.user
    from results.models import Result
    results = Result.objects.filter(student=student).order_by('sem')
    return render(request, 'student/view_results.html', {'student': student, 'results': results})


@login_required
def request_leave(request):
    if request.user.role != 'student':
        return redirect('login')
    student = request.user
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.student = student
            leave.save()
            messages = ['Leave request submitted.']
            return render(request, 'student/leave_request.html', {'form': LeaveRequestForm(), 'messages': messages})
    else:
        form = LeaveRequestForm()
    return render(request, 'student/leave_request.html', {'form': form})
