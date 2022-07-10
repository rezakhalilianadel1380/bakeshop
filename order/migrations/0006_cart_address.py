# Generated by Django 4.0.5 on 2022-07-05 11:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accountt', '0008_delete_user_favorite_breads'),
        ('order', '0005_alter_cart_delivery_mode_alter_cart_payment_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accountt.address'),
        ),
    ]
