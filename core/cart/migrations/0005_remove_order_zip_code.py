# Generated by Django 5.0.2 on 2024-02-27 12:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_remove_order_first_name_remove_order_last_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='zip_code',
        ),
    ]