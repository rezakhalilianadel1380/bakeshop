# Generated by Django 4.0.5 on 2022-07-19 06:23

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bread', '0003_bread_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bread',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
