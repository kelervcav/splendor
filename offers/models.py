from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from user_profile.models import User


# Create your models here.
def file_size(value): # add this to some file where you can import it from
    limit = 2 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 2MB.')


class Offer(models.Model):
    title = models.CharField(max_length=100)
    code = models.CharField(unique=True, max_length=50)
    created_at = models.DateTimeField(default=timezone.now)
    is_offer_active = models.BooleanField(default=False)
    is_used = models.BooleanField(default=False)
    offer_image = models.ImageField(upload_to='images/', validators=[file_size])
    percentage_discount = models.IntegerField(default=None)

    def __str__(self):
        return {self.title}

    class Meta:
        db_table = 'offers'
        permissions = [
            ("disable_offer", "Can disable offer"),
        ]



