# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0036_auto_20150121_1513'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventoryitem',
            name='location',
        ),
        migrations.DeleteModel(
            name='InventoryItemLocation',
        ),
        migrations.RemoveField(
            model_name='inventoryitem',
            name='manufacturer',
        ),
        migrations.DeleteModel(
            name='Manufacturer',
        ),
    ]
