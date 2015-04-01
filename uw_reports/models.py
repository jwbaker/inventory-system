from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


class Report(models.Model):
    class Meta:
        permissions = (
            ('view_all_reports', 'Can view all reports'),
        )

    creator = models.ForeignKey(
        User,
        blank=True,
        default=None,
        null=True,
        related_name='creator'
    )
    creation_date = models.DateField(default=datetime.now)
    view_count = models.PositiveIntegerField(default=0)

    name = models.CharField(max_length=255)
    report_data = models.TextField()
    owner = models.ForeignKey(
        User,
        blank=True,
        default=None,
        null=True,
        related_name='owner'
    )
