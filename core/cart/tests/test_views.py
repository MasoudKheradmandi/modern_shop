from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages

from model_bakery import baker

from account.models import User , Profile
from cart.models import Order , OrderItem
from product.models import Product , TvSize


class TestAddToCart(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = baker.make(User)
        cls.profile = Profile.objects.get(user=cls.user)
        cls.order = baker.make(Order,profile=cls.profile,in_proccesing=False)

        cls.product_show = baker.make(Product,is_show=True)
        cls.product_not_show = baker.make(Product,is_show=False)


        cls.product_variation_a1 = baker.make(TvSize,product=cls.product_show,size='1',count=2)
        cls.product_variation_a2 = baker.make(TvSize,product=cls.product_show,size='2',count=3)
        cls.product_variation_b1 = baker.make(TvSize,product=cls.product_not_show)
        cls.order_item = baker.make(OrderItem,order=cls.order,product_variant=cls.product_variation_a1)

        cls.url = reverse("cart:add-to-cart")
        cls.failure_msg = 'some error caused.pleas try again later'

    def test_empty_request(self):
        response = self.client.get(self.url)
        messages = list(get_messages(response.wsgi_request))

        # self.assertIn(self.failure_msg,str(messages[0]))

    def test_wrong_request(self):
        data_1 = {"quantity":3,'product_variant':self.product_variation_a1} # quantity more than stock
        data_2 = {"quantity":0,'product_variant':self.product_variation_a1} # zero quantity
        data_3 = {"quantity":2,'product_variant':self.product_variation_b1} # product with is_show=False requested

        response_1 = self.client.get(self.url,data=data_1)
        response_2 = self.client.get(self.url,data=data_2)
        response_3 = self.client.get(self.url,data=data_3)

        messages_1 = list(get_messages(response_1.wsgi_request))
        messages_2 = list(get_messages(response_2.wsgi_request))
        messages_3 = list(get_messages(response_3.wsgi_request))

        # self.assertIn(self.failure_msg,str(messages_1[0]))
        # self.assertIn(self.failure_msg,str(messages_2[0]))
        # self.assertIn(self.failure_msg,str(messages_3[0]))

    def test_form_right_data_exist_cart(self):
        data_1 = {'quantity':2,'product_variant':self.product_variation_a1.id}

        self.client.force_login(self.user)
        response_1 = self.client.get(self.url,data=data_1)
        messages_1 = list(get_messages(response_1.wsgi_request))

        self.assertEqual('این محصول در سبد خرید شما وجود دارد',str(messages_1[0]))

    def test_form_right_data_none_exist_cart(self):
        data_2 = {'quantity':2,'product_variant':self.product_variation_a2.id}

        self.client.force_login(self.user)
        response_2 = self.client.get(self.url,data=data_2)
        messages_2 = list(get_messages(response_2.wsgi_request))

        self.assertEqual('این محصول با موفقیت به سبد محصول شما اضافه شد',str(messages_2[0]))


class TestCartListView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("cart:cart-list")
        cls.user = baker.make(User)
        cls.profile = Profile.objects.get(user=cls.user)
        cls.product = baker.make(Product,_fill_optional=True,_create_files=True)
        cls.product_variation = baker.make(TvSize,product=cls.product,count=2)



    def test_empty_cart(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        self.assertTemplateUsed(response,'cart-empty.html')
        self.assertEqual(Order.objects.count(),1)


    def test_list_cart(self):
        order = baker.make(Order,profile=self.profile,in_proccesing=False)
        baker.make(OrderItem,order=order,product_variant=self.product_variation,quantity=1) # WT

        self.client.force_login(self.user)
        response = self.client.get(self.url)

        self.assertTemplateUsed(response,'cart.html')
        self.assertEqual(Order.objects.count(),1)
        self.assertEqual(response.context['order'],order)


class TestDeleteCartItemView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = baker.make(User)
        cls.profile = Profile.objects.get(user=cls.user)
        cls.product = baker.make(Product,_fill_optional=True,_create_files=True)
        cls.product_variation = baker.make(TvSize,product=cls.product,count=2)
        cls.order = baker.make(Order,profile=cls.profile,in_proccesing=False)
        cls.order_item = baker.make(OrderItem,order=cls.order,product_variant=cls.product_variation,quantity=1)

        cls.right_url = reverse("cart:delete-cart-item",kwargs={'order_item_id': cls.order_item.id})
        cls.redirected_url = reverse("cart:cart-list")
        cls.success_message = 'محصول با موفقیت از سبد خرید شما حذف شد'
        cls.failure_msg = 'مشکلی در سیستم رخ داده است. لطفا بعدا دوباره امتحان کنید.'


    def test_wrong_url(self):
        self.client.force_login(self.user)

        response = self.client.get('/cart/delete-cart-item/100/')
        messages = get_messages(response.wsgi_request)

        self.assertEqual(len(messages),1)
        self.assertEqual(self.failure_msg,list(messages)[0].message)
        self.assertEqual('error',list(messages)[0].tags)

        self.assertRedirects(response,self.redirected_url)


    def test_another_user_delete_item(self):
        user_2 = baker.make(User)
        self.client.force_login(user_2)

        response = self.client.get(self.right_url)
        messages = get_messages(response.wsgi_request)

        self.assertEqual(len(messages),1)
        self.assertEqual(self.failure_msg,list(messages)[0].message)
        self.assertEqual('error',list(messages)[0].tags)

        self.assertRedirects(response,self.redirected_url)


    def test_right_url_and_user(self):
        self.client.force_login(self.user)

        response = self.client.get(self.right_url)
        messages = get_messages(response.wsgi_request)

        self.assertEqual(len(messages),1)
        self.assertEqual(self.success_message,list(messages)[0].message)
        self.assertEqual('success',list(messages)[0].tags)

        self.assertRedirects(response,self.redirected_url)


class TestChangeOrderItemQuantityView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = baker.make(User)
        cls.url = reverse('cart:change-cart-quantity')
        cls.product_variation = baker.make(TvSize)
        cls.success_message = 'تعداد محصول با موفقیت تغییر کرد'
        cls.failure_msg = 'مشکلی در سیستم رخ داده است. لطفا بعدا دوباره امتحان کنید.'



    def test_empty_body(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)
        self.assertJSONEqual(str(response.content, encoding='utf8'),{'msg': self.failure_msg})


    def test_right_data(self):
        data = {'quantity':2,'product_variant':self.product_variation.id}

        self.client.force_login(self.user)
        response = self.client.get(self.url,data=data)
        self.assertJSONEqual(str(response.content, encoding='utf8'),{'msg': self.success_message})


class TestShippingView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = baker.make(User)
        cls.url = reverse('cart:shipping-page')

        cls.product = baker.make(Product,is_show=True,_fill_optional=True,_create_files=True)
        cls.product_variation_1 = baker.make(TvSize,product=cls.product,size='1',count=2)
        cls.product_variation_2 = baker.make(TvSize,product=cls.product,size='2',count=3)

        cls.success_message = 'تعداد محصول با موفقیت تغییر کرد'
        cls.failure_msg = 'مشکلی در سیستم رخ داده است. لطفا بعدا دوباره امتحان کنید.'


    def test_empty_cart(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        self.assertTemplateUsed(response,'cart-empty.html')


    def test_in_proccesing_cart(self):
        profile = Profile.objects.get(user=self.user)
        order = baker.make(Order,profile=profile,in_proccesing=True)
        order_item = baker.make(OrderItem,order=order,product_variant=self.product_variation_1,quantity=1)

        self.client.force_login(self.user)
        response = self.client.get(self.url)

        self.assertTemplateUsed(response,'cart-empty.html')


    def test_no_in_proccesing_cart(self):
        profile = Profile.objects.get(user=self.user)
        order = baker.make(Order,profile=profile,in_proccesing=False)
        order_item1 = baker.make(OrderItem,order=order,product_variant=self.product_variation_1,quantity=1)
        order_item2 = baker.make(OrderItem,order=order,product_variant=self.product_variation_2,quantity=1)

        first_variation_price = self.product.price + order_item1.product_variant.price_difference
        second_variation_price = self.product.price + order_item2.product_variant.price_difference

        final_price = first_variation_price + second_variation_price

        self.client.force_login(self.user)
        response = self.client.get(self.url)

        self.assertTemplateUsed(response,'shipping-payment.html')
        self.assertEqual(response.context['order'],order)
        self.assertEqual(response.context['paid_amount_needed'],final_price)


