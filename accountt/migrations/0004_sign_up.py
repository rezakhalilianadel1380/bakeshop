# Generated by Django 4.0.5 on 2022-06-14 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accountt', '0003_alter_code_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='sign_up',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=11, unique=True)),
                ('code', models.CharField(max_length=6, unique=True)),
            ],
        ),
    ]