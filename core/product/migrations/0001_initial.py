# Generated by Django 5.0.1 on 2024-01-30 10:45

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='نام دسته بندی')),
                ('image', models.ImageField(upload_to='', verbose_name='عکس دسته بندی')),
            ],
        ),
        migrations.CreateModel(
            name='DiscountCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField()),
                ('code_name', models.CharField(max_length=30)),
                ('discountـpercent', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(default=1000, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=450, verbose_name='نام محصول')),
                ('image', models.ImageField(upload_to='', verbose_name='عکس محصول')),
                ('sales_number', models.IntegerField(default=0)),
                ('price', models.PositiveIntegerField()),
                ('specification', models.TextField()),
                ('description', models.TextField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True, null=True)),
                ('is_special', models.BooleanField(default=False)),
                ('is_show', models.BooleanField(default=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product.category')),
            ],
        ),
        migrations.CreateModel(
            name='TvSize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=4, verbose_name='سایز')),
                ('price_difference', models.IntegerField(default=0, verbose_name='اختلاف قیمت')),
                ('count', models.PositiveIntegerField()),
                ('discount', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.discountcode')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product.product')),
            ],
        ),
    ]
