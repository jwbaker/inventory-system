# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0032_auto_20150119_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventoryitem',
            name='location',
            field=models.ForeignKey(default=None, blank=True, to='uw_inventory.InventoryItemLocation', null=True),
        ),
    ]
