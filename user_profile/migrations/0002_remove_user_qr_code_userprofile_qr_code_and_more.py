# Generated by Django 4.2.5 on 2023-11-13 14:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='qr_code',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='qr_code',
            field=models.ImageField(blank=True, null=True, upload_to='qr_codes/'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='account_expiry',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 12, 14, 53, 8, 967031)),
        ),
    ]