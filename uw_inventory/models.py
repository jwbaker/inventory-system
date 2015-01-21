from datetime import datetime

from django.db import models


class AutocompleteData(models.Model):
    KIND_CHOICES = [
        ('location', 'location'),
        ('manufacturer', 'manufacturer')
    ]
    name = models.CharField(max_length=255)
    kind = models.CharField(choices=KIND_CHOICES, max_length=255)


# Create your models here.
class InventoryItem(models.Model):
    STATUS_CHOICES = [
        ('SA', 'Stay'),
        ('SO', 'Storage'),
        ('SU', 'Surplussed'),
        ('LO', 'Lost'),
        ('DI', 'Disposed')
    ]

    @staticmethod
    def get_status_display(status_key):
        '''
        Looks up the display text of a given status key.

        Positional arguments:
            status_key -- The value of a status field.
                            One of: '', STATUS_OTHER, STATUS_SURPLUS,
                            STATUS_STORAGE, or STATUS_STAY
        '''
        if status_key:
            return [v[1] for i, v in enumerate(InventoryItem.STATUS_CHOICES)
                    if v[0] == status_key][0]
        # We return '' rather than None because the combination of Django and
        # JavaScript used in the detail page renders None as 'None' (a string)
        return ''

    # These fields get automatically filled and cannot be edited
    creation_date = models.DateField(default=datetime.now)
    deleted = models.BooleanField(default=False)

    # These fields are supplied by the user
    csa_cost = models.IntegerField(blank=True, default=None, null=True)
    csa_required = models.BooleanField(default=False)
    csa_special = models.BooleanField(default=False)
    csa_special_date = models.DateField(blank=True, default=None, null=True)
    description = models.TextField(blank=True, null=True)
    factory_csa = models.BooleanField(default=False)
    location = models.ForeignKey(
        AutocompleteData,
        blank=True,
        default=None,
        null=True,
        related_name='locations'
    )
    lifting_device = models.BooleanField(default=False)
    manufacture_date = models.DateField(blank=True, default=None, null=True)
    manufacturer = models.ForeignKey(
        AutocompleteData,
        blank=True,
        default=None,
        null=True,
        related_name='manufacturers'
    )
    modified_since_csa = models.BooleanField(default=False)
    name = models.CharField(max_length=200)
    purchase_date = models.DateField(blank=True, default=None, null=True)
    purchase_price = models.IntegerField(blank=True, default=None, null=True)
    replacement_cost = models.IntegerField(blank=True, default=None, null=True)
    replacement_cost_date = models.DateField(
        blank=True,
        default=None,
        null=True
    )
    status = models.CharField(
        choices=STATUS_CHOICES,
        default='SA',
        max_length=2,
    )
    undergraduate = models.BooleanField(default=False)
