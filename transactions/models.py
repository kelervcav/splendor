from django.db import models
from django.utils import timezone
from user_profile.models import User
# Create your models here.


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    referenced_id = models.CharField(unique=True, max_length=200, default=None)
    price_amount = models.DecimalField(max_digits=8, decimal_places=2)
    date_added = models.DateField(auto_now_add=True)
    points = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return self.user

    class Meta:
        db_table = 'transactions'
