# Generated by Django 5.0 on 2024-01-03 09:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_cartitems_price1'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitems',
            name='price1',
        ),
    ]