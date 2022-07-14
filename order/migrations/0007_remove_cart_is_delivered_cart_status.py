# Generated by Django 4.0.5 on 2022-07-12 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_cart_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='is_delivered',
        ),
        migrations.AddField(
            model_name='cart',
            name='status',
            field=models.CharField(blank=True, choices=[('1', 'در انتظار پرداخت'), ('2', 'در انتظار تولید'), ('3', 'در حال تولید'), ('4', 'تولید شده '), ('5', 'تحویل داده شده')], default='1', max_length=1),
        ),
    ]
