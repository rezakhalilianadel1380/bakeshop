# Generated by Django 4.0.5 on 2022-08-08 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accountt', '0011_remove_user_detail_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sign_up',
            name='code',
            field=models.CharField(max_length=6),
        ),
    ]
