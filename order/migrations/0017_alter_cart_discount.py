# Generated by Django 4.0.5 on 2023-01-12 11:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0016_alter_discount_discount_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='discount',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.discount'),
        ),
    ]
