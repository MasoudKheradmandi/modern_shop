from django.test import TestCase
from .models import NewsLatter
# Create your tests here.


class MyModelTest(TestCase):
    def setUp(self) -> None:
        self.my_obj = NewsLatter(email='test@gmail.com')

    def test_str_models(self):
        self.assertEqual(str(self.my_obj),'test@gmail.com')