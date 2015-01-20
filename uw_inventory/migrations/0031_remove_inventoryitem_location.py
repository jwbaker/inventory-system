# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0030_inventoryitem_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventoryitem',
            name='location',
        ),
    ]
