# Generated by Django 5.0.1 on 2024-02-05 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_wishlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]