import random , string

from django.db import models
from django.db.models import Sum , F

import jdatetime

class Order(models.Model):
    shopping_id = models.SlugField(unique=True, blank=True,null=True,db_index=True)
    profile = models.ForeignKey('account.Profile',on_delete=models.CASCADE)
    full_name = models.CharField(max_length=250,null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    phone_number = models.CharField(max_length=15,null=True,blank=True)
    paid_amount = models.IntegerField(blank=True,null=True)

    in_proccesing = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)
    prepare_product = models.BooleanField(default=False)
    sended = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    cancelled = models.BooleanField(default=False)

    score = models.IntegerField(default=0)

    payment_date = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return str(self.profile) + " ////////// " + str(self.id)

    def calculate_paid_amount_needed(self) -> int:
        order_detail = OrderItem.objects.filter(order=self)
        total_price = order_detail.aggregate(
            total_spent=Sum(
            F('quantity') * (F('product_variant__price_difference') + F('product_variant__product__price')),
            output_field=models.IntegerField()
            )
        )
        return total_price['total_spent']

    @staticmethod
    def start_ship_date() -> str:
        jdatetime.set_locale(jdatetime.FA_LOCALE)
        today = jdatetime.date.today()
        start_delta_time = jdatetime.timedelta(days=4)
        start_date = today + start_delta_time
        formatted_start_date = f"{start_date.year}-{start_date.jmonth()}-{start_date.day}"
        return formatted_start_date

    @staticmethod
    def end_ship_date() -> str:
        jdatetime.set_locale(jdatetime.FA_LOCALE)
        today = jdatetime.date.today()
        finish_delta_time = jdatetime.timedelta(days=8)
        finish_date = today + finish_delta_time
        formatted_finish_date = f"{finish_date.year}-{finish_date.jmonth()}-{finish_date.day}"
        return formatted_finish_date

    @staticmethod
    def calculate_score(paid_amount) -> None:
        return paid_amount / 1000


    def save(self, *args, **kwargs):
        while not self.shopping_id:
            new_shopping_id = ''.join(
                random.sample(string.ascii_letters, 2) +
                random.sample(string.digits, 2) +
                random.sample(string.ascii_letters, 2),
            )

            if not Order.objects.filter(shopping_id=new_shopping_id).exists():
                self.shopping_id = new_shopping_id

        super().save(*args, **kwargs)

    def get_all_quantity(self):
        order_detail = OrderItem.objects.filter(order=self)
        order_item_quantity = order_detail.aggregate(
            total_quantity=Sum(
            F('quantity')
            )
        )
        return order_item_quantity['total_quantity']


class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product_variant = models.ForeignKey('product.TvSize',on_delete=models.CASCADE)
    final_price = models.IntegerField(blank=True,null=True)
    selected_size = models.CharField(max_length=25,null=True,blank=True)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return str(self.order_id) + " ////////// " + self.product_variant.product.name
