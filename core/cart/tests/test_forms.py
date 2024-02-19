from django.test import TestCase
from django.urls import reverse

from model_bakery import baker

from cart.forms import AddToCartForm
from product.models import Product , TvSize , DiscountCode

class TestAddToCartForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.product_show = baker.make(Product,is_show=True)
        cls.product_not_show = baker.make(Product,is_show=False)

        cls.product_variation_a1 = baker.make(TvSize,product=cls.product_show,size='1',count=2)
        cls.product_variation_a2 = baker.make(TvSize,product=cls.product_show,size='2',count=3)
        cls.product_variation_b1 = baker.make(TvSize,product=cls.product_not_show)

        cls.error_message_1 = "some error caused.pleas try again later"
        cls.error_message_2 = "تعداد انتخابی شما بیشتر از موجودی انبار می باشد"


    def test_form_empty_data(self):
        data = {}
        form = AddToCartForm(data)

        self.assertFalse(form.is_valid())
        self.assertIn('__all__',form.errors.keys())
        self.assertEqual(self.error_message_1,form.errors.get('__all__')[0])


    def test_form_wrong_data(self):
        data_1 = {"quantity":3,'product_variant':self.product_variation_a1} # quantity more than stock
        data_2 = {"quantity":0,'product_variant':self.product_variation_a1} # zero quantity
        data_3 = {"quantity":2,'product_variant':self.product_variation_b1} # product with is_show=False requested

        form_1 = AddToCartForm(data_1)
        form_2 = AddToCartForm(data_2)
        form_3 = AddToCartForm(data_3)

        self.assertFalse(form_1.is_valid())
        self.assertIn('__all__',form_1.errors.keys())
        self.assertEqual(self.error_message_2,form_1.errors.get('__all__')[0])

        self.assertFalse(form_2.is_valid())
        self.assertIn('__all__',form_2.errors.keys())
        self.assertEqual(self.error_message_1,form_2.errors.get('__all__')[0])

        self.assertFalse(form_3.is_valid())
        self.assertIn('__all__',form_3.errors.keys())
        self.assertEqual(self.error_message_1,form_3.errors.get('__all__')[0])


    def test_form_right_data(self):
        data = {'quantity':2,'product_variant':self.product_variation_a1}

        form = AddToCartForm(data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.errors,{})


