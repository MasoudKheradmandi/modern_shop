from django.test import TestCase
from model_bakery import baker
from product.models import Product,Category,TvSize,Comment
from django.urls import reverse

# Create your tests here.
class ProductTest(TestCase):
    def setUp(self):
        self.product = baker.make(Product,name='TV1')

    def test_str_obj(self):
        self.assertEqual(str(self.product),'TV1')



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


class ProductListViewTest(TestCase):
    def setUp(self):
        self.product1 = baker.make(Product,name='TV1',id=1000,is_show=True,_fill_optional=True,_create_files=True)
        self.product2 = baker.make(Product,name='TV2',id=1001,is_show=False,_fill_optional=True,_create_files=True)
        self.product3 = baker.make(Product,name='TV3',id=1003,is_show=True,_fill_optional=True,_create_files=True)

    def test_product_list_view(self):
        response = self.client.get(reverse('product:listview'))
        obj = response.context['product_obj']


        self.assertEqual(obj.count(),2)
        self.assertNotEqual(obj.count(),3)
        self.assertTemplateUsed(response,'listview.html')


class ProductDetailViewTest(TestCase):
    def setUp(self):
        self.product =  baker.make(Product,name='TV1',id=1000,is_show=True,_fill_optional=True,_create_files=True)
        self.tv_size = baker.make(TvSize,product = self.product)
        self.tv_size2 = baker.make(TvSize,product = self.product)
    def test_detail_view_obj(self):

        resp = self.client.get(reverse('product:detail',args=[self.product.category.name,self.product.id]))

        self.assertEqual(resp.context['obj'],self.product)

        self.assertTemplateUsed(resp,'detail.html')

        self.assertIn('obj',resp.context)

        self.assertIn(self.tv_size,resp.context['obj_size'])

        for x in resp.context.get('obj_size'):
            self.assertEqual(self.tv_size.product.name,x.product.name)
