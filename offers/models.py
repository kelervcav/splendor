from django.db import models
from django.utils import timezone

from user_profile.models import User


# Create your models here.

class Offer(models.Model):
    title = models.CharField(max_length=100)
    code = models.CharField(unique=True, max_length=50)
    created_at = models.DateTimeField(default=timezone.now)
    is_offer_active = models.BooleanField(default=False)
    is_used = models.BooleanField(default=False)
    offer_image = models.ImageField(upload_to='images/')
    percentage_discount = models.IntegerField(default=None)

    def __str__(self):
        return {self.title}

    class Meta:
        db_table = 'offers'
        permissions = [
            ("disable_offer", "Can disable offer"),
        ]



