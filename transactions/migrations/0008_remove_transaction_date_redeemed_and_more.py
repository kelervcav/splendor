# Generated by Django 4.2.5 on 2023-11-02 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0007_alter_transaction_date_added'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='date_redeemed',
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date_added',
            field=models.DateField(auto_now_add=True),
        ),
    ]
