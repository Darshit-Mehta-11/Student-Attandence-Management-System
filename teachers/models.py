from django.db import models
from accounts.models import CustomUser

# Create your models here.

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Leave', 'Leave'),
    ]

    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    semester = models.PositiveSmallIntegerField(
        choices=[(1,'1st'),(2,'2nd'),(3,'3rd'),(4,'4th')],
        default=1,
        help_text="Semester during which attendance was recorded"
    )
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Absent')

    class Meta:
        unique_together = ('student', 'semester', 'date')
        ordering = ['-semester', '-date']

    def __str__(self):
        return f"{self.date} ({self.status})"


class LeaveRequest(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField()
    reason = models.TextField(blank=True)
    approved = models.BooleanField(default=False)
    requested_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'date')
        ordering = ['-requested_at']

    def __str__(self):
        return f"Leave for {self.student.username} on {self.date} (approved={self.approved})"
