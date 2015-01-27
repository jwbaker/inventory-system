# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('uw_inventory', '0055_auto_20150127_1103'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryitem',
            name='technician',
            field=models.ForeignKey(related_name=b'technicians', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
