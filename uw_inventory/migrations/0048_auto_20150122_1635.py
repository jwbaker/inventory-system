# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0047_inventoryitem_last_modified'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryitem',
            name='model_number',
            field=models.CharField(default=None, max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='inventoryitem',
            name='serial_number',
            field=models.CharField(default=None, max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
