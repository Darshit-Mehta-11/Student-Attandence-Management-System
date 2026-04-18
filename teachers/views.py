import re
from django.shortcuts import render, redirect
from accounts.models import CustomUser
from .models import Attendance, LeaveRequest
from results.models import Result
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta

# Create your views here.

@login_required
def teacher_dashboard(request):
    if request.user.role != 'teacher':
        return redirect('login')
    teacher = request.user
    # gather some student information for display
    students = CustomUser.objects.filter(role='student')
    total_students = students.count()
    pending_leaves = LeaveRequest.objects.filter(approved=False).count()
    # you can expand this context with real data as needed
    return render(request, 'teacher/teacher_dashbord.html', {
        'teacher': teacher,
        'students': students,
        'total_students': total_students,
        'pending_leaves': pending_leaves,
    })


@login_required
def take_attendance(request):
    if request.user.role != 'teacher':
        return redirect('login')
    students = CustomUser.objects.filter(role='student')
    today = date.today().isoformat()

    if request.method == 'POST':
        sem = request.POST.get('semester') or 1
        attend_date = request.POST.get('date')
        # Instead of relying on radio buttons we now use a checkbox per student.
        # If the checkbox is checked we treat the student as Present, otherwise Absent.
        for student in students:
            key = f"status_{student.id}"
            # a checked checkbox will be present in POST, otherwise we consider the student absent
            status = 'Present' if key in request.POST else 'Absent'
            Attendance.objects.update_or_create(
                student=student,
                semester=sem,
                date=attend_date,
                defaults={'status': status},
            )
        attendance_taken = "Attendance saved successfully."
        return render(request, 'teacher/take_attendance.html', {
            'students': students,
            'attendance_taken': attendance_taken,
            'today': attend_date,
        })
    return render(request, 'teacher/take_attendance.html', {'students': students, 'today': today})


@login_required
def leave_requests(request):
    if request.user.role != 'teacher':
        return redirect('login')
    pending = LeaveRequest.objects.filter(approved=False)
    # if no real requests, provide 5 dummy entries for UI demonstration
    if not pending.exists():
        class Dummy:
            def __init__(self, student, date, reason, pk):
                self.student = student
                self.date = date
                self.reason = reason
                self.pk = pk
                self.approved = False
        students = list(CustomUser.objects.filter(role='student')[:6])
        dummy_list = []
        reasons = [
            'Medical leave',
            'Family function',
            'Sick',
            'Personal work',
            'Festival',
            'Other'
        ]
        # spread dates over the past week
        for idx in range(6):
            stu = students[idx] if idx < len(students) else CustomUser(username=f'Student{idx+1}')
            leave_date = date.today() - timedelta(days=idx)
            dummy_list.append(Dummy(stu, leave_date, reasons[idx % len(reasons)], idx+1))
        pending = dummy_list
    return render(request, 'teacher/leave_requests.html', {'pending': pending})

@login_required
def reject_leave(request, pk):
    if request.user.role != 'teacher':
        return redirect('login')
    try:
        leave = LeaveRequest.objects.get(pk=pk)
    except LeaveRequest.DoesNotExist:
        return redirect('leave_requests')
    leave.delete()
    return redirect('leave_requests')


@login_required
def approve_leave(request, pk):
    if request.user.role != 'teacher':
        return redirect('login')
    try:
        leave = LeaveRequest.objects.get(pk=pk)
    except LeaveRequest.DoesNotExist:
        return redirect('leave_requests')
    leave.approved = True
    leave.save()
    # create or update attendance record to Leave
    Attendance.objects.update_or_create(
        student=leave.student,
        semester=1,  # could derive from date or user profile
        date=leave.date,
        defaults={'status': 'Leave'},
    )
    return redirect('leave_requests')
