from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone

# Create your models here.
class Service(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'services'
        permissions = [
            ("disable_service", "Can disable service"),
        ]


class Treatment(models.Model):
    service = models.ForeignKey(Service, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    area = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'treatments'
        permissions = [
            ("disable_treatment", "Can disable treatment"),
        ]
