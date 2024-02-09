from django.test import TestCase
from home.models import NewsLatter , Footer , Navbar  , Slider , SubFooter


class TestNewsLatterModel(TestCase):
    def setUp(self) -> None:
        self.my_obj = NewsLatter.objects.create(email='test@gmail.com')

    def test_str_models(self):
        self.assertEqual(str(self.my_obj),'test@gmail.com')

class TestFooterModel(TestCase):
    def setUp(self) -> None:
        self.my_obj = Footer.objects.create(name='test_name_footer')

    def test_str_models(self):
        self.assertEqual(str(self.my_obj),'test_name_footer')

class TestSubFooterModel(TestCase):
    def setUp(self) -> None:
        footer_obj = Footer.objects.create(name='test_name_footer')
        self.my_obj = SubFooter.objects.create(parent=footer_obj,name='test_name_subfooter',link="#")

    def test_str_models(self):
        self.assertEqual(str(self.my_obj),'test_name_subfooter')

class TestNavbarModel(TestCase):
    def setUp(self) -> None:
        self.my_obj = Navbar.objects.create(name='test_name_navbar',link='#')

    def test_str_models(self):
        self.assertEqual(str(self.my_obj),'test_name_navbar')
