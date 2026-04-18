import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')
django.setup()

from accounts.models import CustomUser
from results.models import Result

def seed_results():
    students = CustomUser.objects.filter(role='student')
    for student in students:
        # Create results for Sem 1 to 6
        for sem_i in range(1, 7):
            # Check if result already exists
            if not Result.objects.filter(student=student, sem=sem_i).exists():
                Result.objects.create(
                    student=student,
                    sem=sem_i,
                    ac_year="2025-26",
                    seo=75 + sem_i,
                    c_sharp=80 - sem_i,
                    php=70 + sem_i,
                    python=85 - sem_i,
                    java=72 + sem_i
                )
                print(f"Created result for {student.username} Sem {sem_i}")

if __name__ == "__main__":
    seed_results()
