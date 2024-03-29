from django.test import TestCase , SimpleTestCase
from django.core.exceptions import ValidationError

from account.models import User ,Profile ,validate_phone_number ,validate_verification_code

# Create your tests here.

class UserModelTest(SimpleTestCase):
    def setUp(self) -> None:
        self.user = User(phone_number="09123456789")


    def test_str_obj(self):
        self.assertEqual(str(self.user),"09123456789")


class ValidatePhoneNumberTest(SimpleTestCase):
    def test_regex_validation(self):
        # start with optional 0|\+98 followed by 9 digits starts with 9
        iran_phone_number_regex_pattern = "^(?:0|\+98)?(9\d{9})$"

        acceptable_phone_number = "0" + "9123456789"
        self.assertRegex(acceptable_phone_number,iran_phone_number_regex_pattern)

        acceptable_phone_number = "+98" + "9123456789"
        self.assertRegex(acceptable_phone_number,iran_phone_number_regex_pattern)

        acceptable_phone_number = "9123456789"
        self.assertRegex(acceptable_phone_number,iran_phone_number_regex_pattern)

        not_acceptable_phone_number = "123456789"
        self.assertNotRegex(not_acceptable_phone_number,iran_phone_number_regex_pattern)


    def test_function_validation(self):
        wrong_phone_number = "123456789"
        self.assertRaises(ValidationError,validate_phone_number,wrong_phone_number)


class ValidateVerificationCodeTest(SimpleTestCase):
    def test_validation(self):
        self.assertRaises(ValidationError,validate_verification_code,100000)
        self.assertRaises(ValidationError,validate_verification_code,999)


class UserManagerTest(TestCase):
    def test_create_user(self):
        self.user = User.objects.create_user(phone_number='09123456789')
        self.assertEqual(User.objects.count(),1)
        self.assertFalse(self.user.is_superuser)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_verified)
        self.assertRaises(ValueError,User.objects.create_user,phone_number='')


    def test_create_superuser(self):
        self.user = User.objects.create_superuser(phone_number='09123456789')
        self.assertEqual(User.objects.count(),1)
        self.assertTrue(self.user.is_superuser)
        self.assertTrue(self.user.is_staff)
        self.assertTrue(self.user.is_verified)
        self.assertRaises(ValueError,User.objects.create_superuser,phone_number='09123456788',is_staff=False)
        self.assertRaises(ValueError,User.objects.create_superuser,phone_number='09123456788',is_superuser=False)


    def test_create_staffuser(self):
        self.user = User.objects.create_staffuser(phone_number='09123456789')
        self.assertEqual(User.objects.count(),1)
        self.assertFalse(self.user.is_superuser)
        self.assertTrue(self.user.is_staff)
        self.assertTrue(self.user.is_verified)
        self.assertRaises(ValueError,User.objects.create_staffuser,phone_number='09123456788',is_staff=False)


class ProfileModelTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(phone_number='09123456789')


    def test_profile_existance(self):
        self.assertTrue(Profile.objects.filter(user=self.user).exists())


    def test_str_obj(self):
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(str(profile),"09123456789")
