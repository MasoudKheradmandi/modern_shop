# Generated by Django 5.0.2 on 2024-02-20 18:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0011_make_id_start_from_1000'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tvsize',
            name='discount',
        ),
        migrations.DeleteModel(
            name='DiscountCode',
        ),
    ]
