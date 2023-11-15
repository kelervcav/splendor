from datetime import datetime
from django.db import models
from django.utils import timezone
from treatments.models import Treatment
from user_profile.models import User
from datetime import time


# Create your models here.
class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date = models.DateField(null=False, blank=False)
    TIME_CHOICES = [
        ("------", "------"),
        (time(10, 0), "10:00 AM"),
        (time(11, 0), "11:00 AM"),
        (time(12, 0), "12:00 PM"),
        (time(13, 0), "1:00 PM"),
        (time(14, 0), "2:00 PM"),
        (time(15, 0), "3:00 PM"),
        (time(16, 0), "4:00 PM"),
        (time(17, 0), "5:00 PM"),
        (time(18, 0), "6:00 PM"),
        (time(19, 0), "7:00 PM"),
        (time(20, 0), "8:00 PM"),
    ]

    time = models.TimeField(choices=TIME_CHOICES)
    treatment = models.ForeignKey(Treatment, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(default=timezone.now())
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.date} {self.time}"

    class Meta:
        db_table = 'appointments'
        permissions = [
            ("approve_appointment", "Can approve appointment")
        ]
