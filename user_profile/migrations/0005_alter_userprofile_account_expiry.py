# Generated by Django 4.2.5 on 2023-10-31 18:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0004_alter_userprofile_account_expiry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='account_expiry',
            field=models.DateField(default=datetime.datetime(2023, 10, 31, 18, 51, 23, 961871)),
        ),
    ]