from django.db import models

# Create your models here.
from django.db import models
from accounts.models import CustomUser


class Notification(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification({self.student.username}: {self.message})"
