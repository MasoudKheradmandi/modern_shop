import random , string

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.


class Order(models.Model):
    shopping_id = models.SlugField(unique=True, blank=True,null=True,db_index=True)
    profile = models.ForeignKey('account.Profile',on_delete=models.CASCADE)
    first_name = models.CharField(max_length=250,null=True,blank=True)
    last_name = models.CharField(max_length=250,null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    phone_number = models.CharField(max_length=15,null=True,blank=True)
    zip_code = models.CharField(max_length=30,null=True)
    paid_amount = models.IntegerField(blank=True,null=True)

    in_proccesing = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)
    prepare_product = models.BooleanField(default=False)
    sended = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    cancelled = models.BooleanField(default=False)

    payment_date = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return str(self.profile) + " ////////// " + str(self.id)

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


class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product_variant = models.ForeignKey('product.TvSize',on_delete=models.CASCADE)
    final_price = models.IntegerField(blank=True,null=True)
    quantity = models.IntegerField()

    def __str__(self):
        return str(self.order_id) + " ////////// " + self.product_variant.product.name
