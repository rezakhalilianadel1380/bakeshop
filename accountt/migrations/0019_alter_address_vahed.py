# Generated by Django 4.0.5 on 2023-01-21 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accountt', '0018_authenticated_code_create_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='vahed',
            field=models.CharField(default=34, max_length=20, null=True),
        ),
    ]
