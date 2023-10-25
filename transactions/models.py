from django.db import models
from django.utils import timezone
from user_profile.models import User
from treatments.models import Treatment
# Create your models here.


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    treatment = models.ForeignKey(Treatment, on_delete=models.DO_NOTHING)
    price_amount = models.IntegerField()
    points = models.IntegerField()
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user}{self.treatment}'

    def add_points(self):
        self.points = self.price_amount / 150
        self.save()

    class Meta:
        db_table = 'transactions'
