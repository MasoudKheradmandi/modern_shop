# Generated by Django 5.0.2 on 2024-02-28 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0007_alter_orderitem_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='score',
            field=models.IntegerField(default=0),
        ),
    ]