from http.cookies import SimpleCookie

from django.test import TestCase
from django.urls import reverse

from account.models import User


class LoginViewUnitTest(TestCase):
    def setUp(self) -> None:
        self.url = reverse('account:login-page')
        self.success_url = reverse('account:login-verification-page')
        self.test_user = User.objects.create_user(phone_number='09123456789',token=1)


    def test_get_method(self):
        client = self.client
        response = client.get(self.url)
        self.assertTemplateUsed(response,'login.html')

        # login user should return to home page
        client.force_login(self.test_user)
        response = client.get(self.url)
        self.assertRedirects(response,reverse('home:index-page'))


    def test_post_method_empty_body(self):
        response = self.client.post(self.url)
        self.assertRedirects(response,self.url)

        self.client.force_login(self.test_user)
        response = self.client.post(self.url)
        self.assertRedirects(response,reverse('home:index-page'))


    def test_post_method_wrong_data(self):
        response = self.client.post(self.url,data={'phone_number':'123456789'})
        self.assertRedirects(response,self.url)


    def test_post_method_registered_user(self):
        user_old_token = self.test_user.token
        user_phone_number = '09123456789'
        response = self.client.post(self.url,data={'phone_number':user_phone_number})
        user_new_token = User.objects.get(phone_number=user_phone_number).token

        self.assertRedirects(response,self.success_url)
        self.assertEqual(User.objects.count(),1)
        self.assertNotEqual(user_old_token,user_new_token)
        self.assertEqual(response.cookies.get('user_phone_number').coded_value,user_phone_number)


    def test_post_method_unregistered_user(self):
        user_phone_number = '09987654321'
        response = self.client.post(self.url,data={'phone_number':user_phone_number})
        user_new_token = User.objects.get(phone_number=user_phone_number).token

        self.assertRedirects(response,self.success_url)
        self.assertEqual(User.objects.count(),2)
        self.assertEqual(response.cookies.get('user_phone_number').coded_value,user_phone_number)
        self.assertIsNotNone(user_new_token)


class LoginVerificationTest(TestCase):
    def setUp(self) -> None:
        self.failure_url = reverse('account:login-page')
        self.url = reverse('account:login-verification-page')
        self.success_url = reverse('account:welcome-page')
        self.user_phone_number = '09123456789'
        self.test_user = User.objects.create_user(phone_number=self.user_phone_number,token=12345,is_verified=False)


    def test_get_method(self):
        client = self.client
        response = client.get(self.url)
        self.assertTemplateUsed(response,'login-verification.html')

        # login user should return to home page
        client.force_login(self.test_user)
        response = client.get(self.url)
        self.assertRedirects(response,reverse('home:index-page'))


    def test_post_method_empty_body(self):
        response = self.client.post(self.url)
        self.assertRedirects(response,self.url)

        # login user should return to home page
        self.client.force_login(self.test_user)
        response = self.client.post(self.url)
        self.assertRedirects(response,reverse('home:index-page'))


    def test_no_cookie_user(self):
        # no cookie user should return to login page
        response = self.client.post(self.url,data={'verify_code':12345})
        self.assertRedirects(response,self.failure_url)


    def test_post_method_existing_user_wrong_token(self):
        self.client.cookies = SimpleCookie({'user_phone_number':self.user_phone_number})
        response = self.client.post(self.url,data={'verify_code':54321})
        user_is_verified = User.objects.get(phone_number=self.user_phone_number).is_verified


        self.assertRedirects(response,self.url)
        self.assertFalse(user_is_verified)


    def test_post_method_existing_user_right_token(self):
        self.client.cookies = SimpleCookie({'user_phone_number':self.user_phone_number})
        response = self.client.post(self.url,data={'verify_code':12345})
        user_is_verified = User.objects.get(phone_number=self.user_phone_number).is_verified


        self.assertRedirects(response,self.success_url)
        self.assertTrue(user_is_verified)


    def test_post_method_none_existing_user(self):
        self.client.cookies = SimpleCookie({'user_phone_number':'09987654321'})
        response = self.client.post(self.url,data={'verify_code':12345})

        self.assertRedirects(response,self.failure_url)


class WelcomePageTest(TestCase):
    def setUp(self) -> None:
        self.home_url = reverse('home:index-page')
        self.url = reverse('account:welcome-page')
        self.user_phone_number = '09123456789'
        self.test_user = User.objects.create_user(phone_number=self.user_phone_number)


    def test_get_method(self):
        resposne = self.client.get(self.url)
        self.assertRedirects(resposne,self.home_url)

        self.client.force_login(self.test_user)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response,'welcome.html')
