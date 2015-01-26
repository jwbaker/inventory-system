# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0050_inventoryitem_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventoryitem',
            name='uuid',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
