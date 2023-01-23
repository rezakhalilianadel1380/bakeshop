# Generated by Django 4.0.5 on 2023-01-23 08:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accountt', '0024_city_state_alter_address_city_alter_address_state'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='city',
            new_name='city_v',
        ),
        migrations.RemoveField(
            model_name='address',
            name='state',
        ),
        migrations.AddField(
            model_name='address',
            name='state_v',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accountt.state'),
        ),
    ]
