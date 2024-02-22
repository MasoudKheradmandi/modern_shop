from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages

from model_bakery import baker

from account.models import User
from cart.models import Order


class TestAddToCart(TestCase):
    def setUp(self) -> None:
        self.order = baker.make(Order)
        self.user = baker.make(User)
        self.url = reverse("cart:add-to-cart")
        self.failure_msg = 'some error caused.pleas try again later'

    def test_empty_request(self):
        response = self.client.get(self.url)
        messages = list(get_messages(response.wsgi_request))

        self.assertIn(self.failure_msg,str(messages[0]))

    def test_wrong_request(self):
        data_1 = {'quantity':-1}
        response = self.client.get(self.url,data=data_1)
        messages = list(get_messages(response.wsgi_request))

        self.assertIn(self.failure_msg,str(messages[0]))
