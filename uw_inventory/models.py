from datetime import date

from django.db import models


# Create your models here.
class InventoryItem(models.Model):
    STATUS_STAY = 'SA'
    STATUS_STORAGE = 'SO'
    STATUS_SURPLUS = 'SU'
    STATUS_OTHER = 'OT'
    STATUS_CHOICES = [
        (STATUS_STAY,    'Stay'),
        (STATUS_STORAGE, 'Storage'),
        (STATUS_SURPLUS, 'Surplussed'),
        (STATUS_OTHER,   'Other'),
    ]

    name = models.CharField(blank=True, max_length=200)
    creation_date = models.DateField(blank=True, default=date.today, null=True)
    description = models.TextField(blank=True)
    status = models.CharField(
        blank=True,
        choices=STATUS_CHOICES,
        default=None,
        max_length=2,
        null=True)
    purchase_price = models.IntegerField(blank=True, null=True)
