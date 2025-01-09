from django.test import TestCase

from django.test import TestCase
from django.contrib.auth.models import User
from intake.models import Submission
from intake.forms import SubmissionForm
from django.urls import reverse

class SubmissionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.submission = Submission.objects.create(
            user=self.user,
            name="John Doe",
            email="johndoe@example.com",
            reason="I feel stressed.",
            preferred_date="2025-01-10",
            preferred_time="14:30:00"
        )

    def test_submission_creation(self):
        self.assertEqual(Submission.objects.count(), 1)
        self.assertEqual(self.submission.name, "John Doe")
        self.assertEqual(self.submission.status, "Pending")

    def test_str_representation(self):
        self.assertEqual(str(self.submission), "John Doe - Pending")


class SubmissionFormTest(TestCase):
    def test_valid_submission_form(self):
        form_data = {
            "name": "Jane Doe",
            "email": "janedoe@example.com",
            "reason": "Need career guidance.",
            "preferred_date": "2025-01-11",
            "preferred_time": "15:00:00"
        }
        form = SubmissionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_submission_form(self):
        form_data = {
            "name": "",  # Missing name
            "email": "invalid-email",  # Invalid email
            "reason": "",
            "preferred_date": "2025-01-11",
            "preferred_time": "15:00:00"
        }
        form = SubmissionForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
        self.assertIn("email", form.errors)


class ViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

    def test_submit_form_view(self):
        response = self.client.get(reverse('submit_form'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'submit_form.html')

    def test_submission_history_view(self):
        Submission.objects.create(
            user=self.user,
            name="John Doe",
            email="johndoe@example.com",
            reason="Stress",
            preferred_date="2025-01-10",
            preferred_time="14:30:00"
        )
        response = self.client.get(reverse('submission_history'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "John Doe")

    def test_admin_dashboard_view(self):
        # Admin user
        admin_user = User.objects.create_superuser(username='admin', password='admin123')
        self.client.login(username='admin', password='admin123')

        Submission.objects.create(
            user=self.user,
            name="John Doe",
            email="johndoe@example.com",
            reason="Stress",
            preferred_date="2025-01-10",
            preferred_time="14:30:00"
        )
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "John Doe")

# Create your tests here.
