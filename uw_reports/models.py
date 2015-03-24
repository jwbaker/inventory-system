from django.db import models

from uw_inventory.models import InventoryItem


class Report(models.Model):
    name = models.CharField(max_length=255)
    report_data = models.TextField()
    owner = models.ForeignKey(
        InventoryItem,
        blank=True,
        default=None,
        null=True
    )
