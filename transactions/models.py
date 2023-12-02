from django.db import models
from django.utils import timezone

from treatments.models import Treatment
from user_profile.models import User
# Create your models here.


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    treatment = models.ForeignKey(Treatment, on_delete=models.DO_NOTHING)
    price_amount = models.DecimalField(max_digits=8, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)
    points = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    offer_code = models.CharField(null=True, max_length=50)
    discounted_amount = models.DecimalField(default=0.00, max_digits=8, decimal_places=2)

    def __str__(self):
        return self.user

    class Meta:
        db_table = 'transactions'


