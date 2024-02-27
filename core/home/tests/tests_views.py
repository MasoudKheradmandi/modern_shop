import pytz

from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from django.utils.timezone import datetime
from model_bakery import baker

from home.models import NewsLatter , SiteSettings
from product.models import Product , Category

class NewsLetterTest(TestCase):
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


class TestHomeView(TestCase):
    def setUp(self) -> None:
        cat_1 = baker.make(Category)
        cat_2 = baker.make(Category)
        self.product_1 = baker.make(Product,updated_date=datetime(year=2002,month=1,day=1,hour=1,minute=1,second=1,tzinfo=pytz.UTC)
                                    ,sales_number=5,category=cat_1,_create_files=True) # new updated
        self.product_2 = baker.make(Product,updated_date=datetime(year=2000,month=1,day=1,hour=1,minute=1,second=1,tzinfo=pytz.UTC)
                                    ,sales_number=7,category=cat_2,_create_files=True) # least popular
        self.product_3 = baker.make(Product,updated_date=datetime(year=2001,month=1,day=1,hour=1,minute=1,second=1,tzinfo=pytz.UTC)
                                    ,sales_number=9,category=cat_1,_create_files=True) # most sales

    def test_home_view(self):
        url = reverse('home:index-page')
        response = self.client.get(url)

        self.assertEqual(response.context.get('all_products')[0],self.product_1)
        self.assertEqual(response.context.get('most_sell_products')[0],self.product_3)
        self.assertEqual(response.context.get('popular_products')[2],self.product_2)

