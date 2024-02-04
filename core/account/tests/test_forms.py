from django.test import TestCase
from django.core.exceptions import ValidationError
from account.forms import LoginForm
from account.models import User


class LoginFormTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(phone_number='09123456789')

    def test_wrong_data_clean_method(self):
        form = LoginForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('phone_number',form.errors.keys())

        form = LoginForm(data={'phone_number':'12'})
        self.assertFalse(form.is_valid())
        self.assertIn('phone_number',form.errors.keys())

    def test_right_data_clean_method(self):
        form = LoginForm(data={'phone_number':'09123456789'})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['user'],self.user)

        form = LoginForm(data={'phone_number':'09987654321'})
        self.assertTrue(form.is_valid())
        self.assertEqual(User.objects.count(),2)
        self.assertFalse(User.objects.get(phone_number='09987654321').is_verified)






