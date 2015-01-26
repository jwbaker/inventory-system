# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0053_auto_20150126_1531'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inventoryitem',
            options={'permissions': (('view_item', 'Can view inventory items'), ('view_deleted_item', 'Can view deleted inventory items'))},
        ),
    ]
