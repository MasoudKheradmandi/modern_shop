# Generated by Django 5.0.2 on 2024-02-15 23:17

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0005_alter_profile_avatar'),
        ('product', '0010_alter_product_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shopping_id', models.SlugField(blank=True, null=True, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=250, null=True)),
                ('last_name', models.CharField(blank=True, max_length=250, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('zip_code', models.CharField(max_length=30, null=True)),
                ('paid_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('in_proccesing', models.BooleanField(default=False)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('prepare_product', models.BooleanField(default=False)),
                ('sended', models.BooleanField(default=False)),
                ('delivered', models.BooleanField(default=False)),
                ('cancelled', models.BooleanField(default=False)),
                ('payment_date', models.DateTimeField(blank=True, null=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.profile')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('final_price', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('calculated_discount', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)])),
                ('quantity', models.IntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cart.order')),
                ('product_variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.tvsize')),
            ],
        ),
    ]
