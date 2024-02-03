from django.test import TestCase , RequestFactory
from django.urls import reverse
from selenium.webdriver.chrome.webdriver import WebDriver

from account.models import User
class LoginViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.url = reverse('account:login-page')
        cls.success_url = reverse('account:login-verification-page')
        cls.test_user = User.objects.create_user(phone_number='09123456789')
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()


    def test_get_method(self):
        client = self.client
        response = client.get(self.url)
        self.assertTemplateUsed(response,'login.html')

        client.force_login(self.test_user)
        response = client.get(self.url)
        self.assertRedirects(response,reverse('home:index-page'))


    def test_post_method_empty_body(self):
        response = self.client.post(self.url)
        self.assertRedirects(response,self.url)

        self.client.force_login(self.test_user)
        response = self.client.get(self.url)
        self.assertRedirects(response,reverse('home:index-page'))


    def test_post_method_wrong_data(self):
        response = self.client.post(self.url,data={'phone_number':'123456789'})
        self.assertRedirects(response,self.url)


    def test_post_method_existing_user(self):
        user_phone_number = '09123456789'
        response = self.client.post(self.url,data={'phone_number':user_phone_number})
        self.assertRedirects(response,self.success_url)
        self.assertEqual(User.objects.count(),1)
        self.assertEqual(response.cookies.get('user_phone_number').coded_value,user_phone_number)


    def test_post_method_none_existing_user(self):
        user_phone_number = '09987654321'
        response = self.client.post(self.url,data={'phone_number':user_phone_number})
        self.assertRedirects(response,self.success_url)
        self.assertEqual(User.objects.count(),2)
        self.assertEqual(response.cookies.get('user_phone_number').coded_value,user_phone_number)






