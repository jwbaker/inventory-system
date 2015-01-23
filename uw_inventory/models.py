from datetime import datetime

from django.core.validators import RegexValidator
from django.db import models


class AutocompleteData(models.Model):
    class Meta:
        # We don't want to have two locations (for instance) with the same name
        unique_together = ('name', 'kind',)
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
    last_modified = models.DateTimeField(
        auto_now=True,
        default=datetime.now
    )
    location = models.ForeignKey(
        AutocompleteData,
        blank=True,
        default=None,
        null=True,
        # Django complains because we have two fields that foreign key to the
        # same table. related_name defines the name of the reverse relation.
        # i.e. InventoryItem.locations.all() returns the set of locations
        # related to the given InventoryItem instance
        related_name='locations'
    )
    lifting_device = models.BooleanField(default=False)
    lifting_device_inspection_date = models.DateField(
        blank=True,
        default=None,
        null=True
    )
    manufacture_date = models.DateField(blank=True, default=None, null=True)
    manufacturer = models.ForeignKey(
        AutocompleteData,
        blank=True,
        default=None,
        null=True,
        related_name='manufacturers'
    )
    model_number = models.CharField(
        blank=True,
        default=None,
        max_length=255,
        null=True,
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
    serial_number = models.CharField(
        blank=True,
        default=None,
        max_length=255,
        null=True,
    )
    sop_required = models.BooleanField(default=True)
    status = models.CharField(
        choices=STATUS_CHOICES,
        default='SA',
        max_length=2,
    )
    tech_id = models.CharField(
        blank=True,
        default=None,
        max_length=255,
        null=True,
        validators=[
            RegexValidator(
                r'[A-Z]{2}-[0-9]*',
                'Must be of the form AA-0000'
            )
        ]
    )
    undergraduate = models.BooleanField(default=False)

    @property
    def uuid(self):
        return "{0}-{1}".format(
            self.creation_date.strftime('%Y%m%d'),
            self.id
        )
