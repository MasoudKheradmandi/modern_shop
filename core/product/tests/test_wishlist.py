from django.test import TestCase
from account.models import User,Profile
from model_bakery import baker
from product.models import Product,WishList
from django.urls import reverse

# Create your tests here.


class WishListTest(TestCase):
    def setUp(self) -> None:
        User.objects.create_user(phone_number='09031234567')
        self.profile = Profile.objects.last()
        self.profile.full_name = "Masoud"
        self.product= baker.make(Product,name='TV1',is_show=True,_fill_optional=True)
        self.item_one = WishList.objects.create(profile=self.profile)
        self.item_one.product.add(self.product)

    def test_str_model(self):
        self.assertEqual(str(self.item_one),'Masoud')