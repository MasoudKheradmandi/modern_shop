# Generated by Django 5.0.1 on 2024-02-03 19:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_alter_tvsize_discount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='title',
        ),
    ]
