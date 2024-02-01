from django.test import TestCase
from django.core.exceptions import ValidationError
from account.forms import LoginForm
from account.models import User


class LoginFormTest(TestCase):
    def setUp(self) -> None:
        User.objects.create_user(phone_number='09123456789')

    def test_wrong_data_clean_method(self):
        form = LoginForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('phone_number',form.errors.keys())

        form = LoginForm(data={'phone_number':'12'})
        self.assertFalse(form.is_valid())
        self.assertIn('phone_number',form.errors.keys())

    def test_right_data_clean_method(self):
        pass   





