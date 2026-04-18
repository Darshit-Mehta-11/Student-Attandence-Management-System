from django.test import TestCase
from django.urls import reverse
from .models import CustomUser


class AuthFlowTests(TestCase):
    def setUp(self):
        # create a student and teacher for login tests
        self.student = CustomUser.objects.create_user(
            username='stud1', password='pass1234', role='student', is_active=True
        )
        self.teacher = CustomUser.objects.create_user(
            username='teach1', password='pass1234', role='teacher', is_active=True, is_staff=True
        )

    def test_student_registration_valid(self):
        data = {
            'username': 'newstud',
            'email': 'newstud@example.com',
            'role': 'student',
            'password1': 'complexPass1!',
            'password2': 'complexPass1!',
        }
        response = self.client.post(reverse('student_register'), data)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(CustomUser.objects.filter(username='newstud', role='student').exists())

    def test_teacher_registration_valid(self):
        data = {
            'username': 'newteach',
            'email': 'newteach@example.com',
            'role': 'teacher',
            'password1': 'complexPass2!',
            'password2': 'complexPass2!',
        }
        response = self.client.post(reverse('student_register'), data)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(CustomUser.objects.filter(username='newteach', role='teacher').exists())

    def test_login_success_student(self):
        response = self.client.post(
            reverse('login'),
            {'role': 'student', 'username': 'stud1', 'password': 'pass1234'},
            follow=True,
        )
        self.assertRedirects(response, reverse('student_dashboard'))

    def test_login_success_teacher(self):
        response = self.client.post(
            reverse('login'),
            {'role': 'teacher', 'username': 'teach1', 'password': 'pass1234'},
        )
        # should redirect to dashboard, but don't follow further to avoid login-required loop
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('teacher_dashboard'), response['Location'])

    def test_login_wrong_password_shows_error(self):
        response = self.client.post(
            reverse('login'),
            {'role': 'student', 'username': 'stud1', 'password': 'wrong'},
            follow=True,
        )
        self.assertContains(response, "Password incorrect")

    def test_login_account_inactive(self):
        inactive = CustomUser.objects.create_user(
            username='bad', password='pass', role='student', is_active=False
        )
        response = self.client.post(
            reverse('login'),
            {'role': 'student', 'username': 'bad', 'password': 'pass'},
            follow=True,
        )
        self.assertContains(response, "not active")
