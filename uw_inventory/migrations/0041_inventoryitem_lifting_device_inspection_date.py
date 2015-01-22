# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0040_auto_20150121_1629'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryitem',
            name='lifting_device_inspection_date',
            field=models.DateField(default=None, null=True, blank=True),
            preserve_default=True,
        ),
    ]
