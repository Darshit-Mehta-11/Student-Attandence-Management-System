from django.contrib import admin
from .models import Attendance, LeaveRequest

# Register your models here.

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'semester', 'status')
    fields = ('student', 'semester', 'date', 'status')
    list_filter = ('semester', 'status')
    search_fields = ('student__username', 'student__email', 'date')


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'approved', 'requested_at')
    list_filter = ('approved',)
    search_fields = ('student__username',)
    actions = ['approve_requests']

    def approve_requests(self, request, queryset):
        queryset.update(approved=True)
        # optionally create attendance records
        for leave in queryset:
            Attendance.objects.update_or_create(
                student=leave.student,
                semester=1,  # default or compute from leave.date?
                date=leave.date,
                defaults={'status': 'Leave'},
            )
    approve_requests.short_description = "Approve selected leave requests"

