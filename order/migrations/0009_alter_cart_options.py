# Generated by Django 4.0.5 on 2022-07-26 15:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_alter_cart_delivery_mode'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'permissions': [('can_view_cart', 'میتونه سفارش ها رو مشاهده کنه')]},
        ),
    ]