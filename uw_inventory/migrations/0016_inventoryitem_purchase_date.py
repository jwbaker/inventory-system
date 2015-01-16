# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0015_inventoryitem_manufacture_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryitem',
            name='purchase_date',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
