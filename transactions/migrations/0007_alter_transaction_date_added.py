# Generated by Django 4.2.5 on 2023-11-01 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0006_transaction_date_redeemed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]