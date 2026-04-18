
from django.db import models
# Create your models here.
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    # roll number automatically assigned for students; unique so each student gets a distinct value
    rollno = models.PositiveIntegerField(blank=True, null=True, unique=True)
    stream = models.CharField(max_length=30, default='Not selected')
    
    def save(self, *args, **kwargs):
        # when a student record is saved without a roll number, assign next available
        if self.role == 'student' and not self.rollno:
            # find the maximum rollno among existing students
            from django.db.models import Max
            max_roll = CustomUser.objects.filter(role='student').aggregate(Max('rollno'))['rollno__max'] or 0
            self.rollno = max_roll + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
