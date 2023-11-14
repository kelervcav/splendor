from datetime import datetime
from django.db import models
from django.utils import timezone
from treatments.models import Treatment
from user_profile.models import User


# Create your models here.
class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date = models.DateField(null=False, blank=False)
    TIME_CHOICES = [
        ("------", "------"),
        ("10 AM", "10:00 AM"),
        ("11 AM", "11:00 AM"),
        ("12 PM", "12:00 PM"),
        ("1 PM", "1:00 PM"),
        ("2 PM", "2:00 PM"),
        ("3 PM", "3:00 PM"),
        ("4 PM", "4:00 PM"),
        ("5 PM", "5:00 PM"),
        ("6 PM", "6:00 PM"),
        ("7 PM", "7:00 PM"),
        ("8 PM", "8:00 PM"),
    ]
    time = models.CharField(max_length=10, choices=TIME_CHOICES)
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
