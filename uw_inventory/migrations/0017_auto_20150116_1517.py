# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0016_inventoryitem_purchase_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryitem',
            name='replacement_cost',
            field=models.IntegerField(default=None, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='inventoryitem',
            name='manufacture_date',
            field=models.DateField(default=None, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='inventoryitem',
            name='purchase_date',
            field=models.DateField(default=None, null=True, blank=True),
        ),
    ]
