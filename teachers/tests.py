from django.test import TestCase
from django.urls import reverse
from accounts.models import CustomUser


class TeacherDashboardTests(TestCase):
    def setUp(self):
        # create a teacher and some students
        self.teacher = CustomUser.objects.create_user(
            username='t1', password='pass', role='teacher', is_active=True, is_staff=True
        )
        # ensure role saved correctly (debug)
        assert self.teacher.role == 'teacher', f"teacher role was {self.teacher.role}"
        self.students = []
        for i in range(3):
            self.students.append(
                CustomUser.objects.create_user(
                    username=f'stud{i}', password='pass', role='student', is_active=True
                )
            )

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('teacher_dashboard'))
        self.assertEqual(response.status_code, 302)  # redirected to login

    def test_dashboard_shows_students(self):
        # perform a normal login so middleware sets session correctly
        login_data = {'role': 'teacher', 'username': 't1', 'password': 'pass'}
        resp = self.client.post(reverse('login'), login_data)
        self.assertEqual(resp.status_code, 302)
        # after login POST, check which user is in request
        user_after = resp.wsgi_request.user
        self.assertTrue(user_after.is_authenticated)
        self.assertEqual(user_after.role, 'teacher')
        # inspect session
        session = self.client.session
        self.assertEqual(str(self.teacher.pk), session.get('_auth_user_id'))
        # now follow the redirect manually to get dashboard
        response = self.client.get(reverse('teacher_dashboard'))
        self.assertEqual(response.status_code, 200)
        # check that at least one student username is in the response
        self.assertContains(response, self.students[0].username)
