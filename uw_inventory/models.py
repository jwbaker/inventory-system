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
    deleted = models.BooleanField(default=False)

    @staticmethod
    def get_status_display(status_key):
        '''
        Looks up the display text of a given status key

        Positional arguments:
            status_key -- The value of a status field.
                            One of: '', STATUS_OTHER, STATUS_SURPLUS,
                            STATUS_STORAGE, or STATUS_STAY
        '''
        if status_key:
            return [v[1] for i, v in enumerate(InventoryItem.STATUS_CHOICES)
                    if v[0] == status_key]
        # We return '' rather than None because the combination of Django and
        # JavaScript used in the detail page renders None as 'None' (a string)
        return ''
