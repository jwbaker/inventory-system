from datetime import datetime

from django.db import models

from uw_inventory.models import InventoryItem


class Report(models.Model):
    creator = models.ForeignKey(
        InventoryItem,
        blank=True,
        default=None,
        null=True,
        related_name='creator'
    )
    creation_date = models.DateField(default=datetime.now)

    name = models.CharField(max_length=255)
    report_data = models.TextField()
    owner = models.ForeignKey(
        InventoryItem,
        blank=True,
        default=None,
        null=True,
        related_name='report_owner'
    )
