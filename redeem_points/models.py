from django.db import models
from django.utils import timezone
from user_profile.models import User


# Create your models here.
class RedeemPoints(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date_redeemed = models.DateTimeField(default=timezone.now)
    redeemed_points = models.IntegerField(default=0)

    def __str__(self):
        return self.user

    class Meta:
        db_table = 'redeemed_points'
