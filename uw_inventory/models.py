from django.db import models


# Create your models here.
class InventoryItem(models.Model):
    STATUS_STAY = 'SA'
    STATUS_STORAGE = 'SO'
    STATUS_SURPLUS = 'SU'
    STATUS_OTHER = 'OT'
    STATUS_CHOICES = [
        ('', ''),
        (STATUS_STAY,    'Stay'),
        (STATUS_STORAGE, 'Storage'),
        (STATUS_SURPLUS, 'Surplussed'),
        (STATUS_OTHER,   'Other'),
    ]

    # We're going to loop over this to make it easier for us to save items
    # This is why we expect the control element to have a label that can be
    # converted into an attribute name
    EDITABLE_FIELDS = [
        'description',
        'name',
        'purchase_price',
        'status',
    ]

    NUMERIC_FIELDS = [
        'purchase_price',
    ]

    name = models.CharField(max_length=200)
    creation_date = models.DateField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        blank=True,
        choices=STATUS_CHOICES,
        default=None,
        max_length=2,
        null=True)
    purchase_price = models.IntegerField(blank=True, default=None, null=True)
