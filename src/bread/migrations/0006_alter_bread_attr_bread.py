# Generated by Django 4.2.7 on 2023-12-16 12:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bread', '0005_rename_price_bread_base_price_bread_is_attr_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bread_attr',
            name='bread',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bread_attr', to='bread.bread'),
        ),
    ]
