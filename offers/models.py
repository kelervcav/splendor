from django.db import models
from django.utils import timezone

from user_profile.models import User


# Create your models here.

class Discount(models.Model):
    title = models.CharField(max_length=100)
    code = models.CharField(unique=True, max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(default=timezone.now)
    is_discount_active = models.BooleanField(default=False)
    offer_image = models.ImageField(upload_to='images/')

    def __str__(self):
        return {self.title}

    class Meta:
        db_table = 'offers'
