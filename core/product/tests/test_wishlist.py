from django.test import TestCase
from account.models import User,Profile
from model_bakery import baker
from product.models import Product,WishList
from django.urls import reverse
from django.contrib.messages import get_messages

# Create your tests here.


class WishListTest(TestCase):
    def setUp(self) -> None:
        self.user=User.objects.create_user(phone_number='09031234567')
        self.profile = Profile.objects.last()
        self.profile.full_name = "Masoud"
        self.product= baker.make(Product,name='TV1',is_show=True,_fill_optional=True,_create_files=True)


    def test_str_model(self):
        self.item_one = WishList.objects.create(profile=self.profile)
        self.item_one.product.add(self.product)
        self.item_one.save()

        self.assertEqual(str(self.item_one),'Masoud')

    
    def test_view_wish_list_item_in_signin_mode(self):
        self.client.force_login(self.user)
        item_one = WishList.objects.create(profile=self.profile)
        item_one.product.add(self.product.id)
        item_one.save()

        url = reverse('product:wish_list')
        resp=self.client.get(url)

        self.assertIn('products',resp.context)
        self.assertTemplateUsed(resp,'wishlist.html')
        self.assertEqual(resp.context['products'].count(),1)

    def test_view_wishlist_no_item_in_sign_in_mode(self):
        self.client.force_login(self.user)

        url = reverse('product:wish_list')
        resp=self.client.get(url)

        self.assertIn('obj_count',resp.context)
        self.assertIn('msg',resp.context)

        msg =  'سبد علاقمندی های شما خالی است'
        self.assertEqual(str(resp.context['msg']),msg)
  
    
    def test_view_wish_in_signout_mode(self):
        url = reverse('product:wish_list')
        resp=self.client.get(url)
        
        messages = list(get_messages(resp.wsgi_request))
        self.assertEqual(len(messages),1)
        self.assertEqual(str(messages[0]),'ابتدا وارد حساب کاربری خود شوید')