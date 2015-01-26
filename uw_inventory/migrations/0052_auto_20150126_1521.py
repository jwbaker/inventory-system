# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0051_auto_20150126_1135'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inventoryitem',
            options={'permissions': (('view_item', 'Can view Inventory Items'),)},
        ),
    ]
