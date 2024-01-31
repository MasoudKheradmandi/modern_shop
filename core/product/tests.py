from django.test import TestCase
from model_bakery import baker
from .models import Product,Category,DiscountCode,TvSize,Comment


# Create your tests here.
class ProductTest(TestCase):
    def setUp(self):
        self.product = baker.make(Product,name='TV1')

    def test_str_obj(self):
        self.assertEqual(str(self.product),'TV1')



class DiscountTest(TestCase):
    def setUp(self):
        self.discount = baker.make(DiscountCode,code_name='index1212',count=2)

    def test_str_obj(self):
        self.assertEqual(str(self.discount),"index1212" + " "+"2")

class CategoryTest(TestCase):
    def setUp(self):
        self.cat = baker.make(Category,name='SAMSUNG')
    
    def test_str_obj(self):
        self.assertEqual(str(self.cat),'SAMSUNG')

class TvSizeTest(TestCase):
    def setUp(self):
        self.tv = baker.make(TvSize,product__name='TV1',size='32')

    def test_str_obj(self):
        self.assertEqual(str(self.tv),'TV1 32')


class CommentTest(TestCase):
    def setUp(self):
        self.comm = baker.make(Comment,product__name='TV1',title='test',is_show=bool(True))

    def test_str_obj(self):
        self.assertEqual(str(self.comm),'test TV1 '+ self.is_show)