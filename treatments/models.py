from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone


# Create your models here.
class Service(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255, default=None, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, default='Available')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'services'


class TreatmentArea(models.Model):
    area = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, default='Available')

    def __str__(self):
        return self.area

    class Meta:
        db_table = 'treatment_areas'


class PriceType(models.Model):
    type = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, default='Available')

    def __str__(self):
        return self.type

    class Meta:
        db_table = 'price_types'


class Treatment(models.Model):
    service = models.ForeignKey(Service, on_delete=models.DO_NOTHING)
    area = models.ForeignKey(TreatmentArea, on_delete=models.DO_NOTHING)
    type = models.ForeignKey(PriceType, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, default='Available')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'treatments'
