from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages

from home.models import NewsLatter , SiteSettings


class MyModelTest(TestCase):
    def setUp(self) -> None:
        self.test_email = 'test@test.com'
        self.news_letter = NewsLatter.objects.create(email='test@test.com')
        self.url = reverse('home:footer-layout')
        self.success_message = 'ایمیل شما با موفقیت ثبت شد.'
        self.failure_message = 'مشکلی پیش امده است لطفا دوباره تلاش کنید.'


    def test_not_valid_post_method(self):
        data = {'email':'1234'}
        response = self.client.post(self.url,data)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(messages[0].message,self.failure_message)


    def test_valid_post_method(self):
        data = {'email':'test@test.com'}
        response = self.client.post(self.url,data)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(messages[0].message,self.success_message)



