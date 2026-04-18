from django.test import TestCase
from django.urls import reverse
from accounts.models import CustomUser
from teachers.models import LeaveRequest


class LeaveFlowTests(TestCase):
    def setUp(self):
        self.student = CustomUser.objects.create_user(
            username='s1', password='pass', role='student', is_active=True
        )
        self.teacher = CustomUser.objects.create_user(
            username='t1', password='pass', role='teacher', is_active=True, is_staff=True
        )

    def test_student_can_request_leave(self):
        self.client.login(username='s1', password='pass')
        data = {'date': '2025-10-10', 'reason': 'Doctor appointment'}
        response = self.client.post(reverse('request_leave'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(LeaveRequest.objects.filter(student=self.student, date='2025-10-10').exists())

    def test_teacher_can_approve_leave(self):
        # student makes request
        leave = LeaveRequest.objects.create(student=self.student, date='2025-11-01', reason='Sick')
        # teacher approves via view
        self.client.login(username='t1', password='pass')
        response = self.client.get(reverse('approve_leave', args=[leave.pk]))
        self.assertRedirects(response, reverse('leave_requests'))
        leave.refresh_from_db()
        self.assertTrue(leave.approved)
