# Generated by Django 4.0.5 on 2022-08-08 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accountt', '0012_alter_sign_up_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='code',
            name='code',
            field=models.CharField(max_length=6),
        ),
    ]
