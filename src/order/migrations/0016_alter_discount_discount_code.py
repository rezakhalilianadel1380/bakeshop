# Generated by Django 4.0.5 on 2022-09-03 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0015_alter_cart_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='discount_code',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
