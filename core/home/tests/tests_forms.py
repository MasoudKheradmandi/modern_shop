from django.test import TestCase

from home.models import NewsLatter
from home.forms import NewsLetterForm
# Create your tests here.


class MyModelTest(TestCase):
    def setUp(self) -> None:
        self.test_email = 'test@test.com'
        self.news_letter = NewsLatter.objects.create(email='test@test.com')

    def test_form_wrong_data(self):
        data = {'email':''}
        form = NewsLetterForm(data)
        self.assertFalse(form.is_valid())

        data = {'email':'1234'}
        form = NewsLetterForm(data)
        self.assertFalse(form.is_valid())

    def test_form_right_data_existing_news_letter(self):
        data = {'email':self.test_email}
        form = NewsLetterForm(data)
        self.assertTrue(form.is_valid())
        self.assertEqual(NewsLatter.objects.count(),1)

    def test_form_right_data_none_existing_news_letter(self):
        data = {'email':'test2@gmail.com'}
        form = NewsLetterForm(data)
        self.assertTrue(form.is_valid())
        self.assertEqual(NewsLatter.objects.count(),2)






