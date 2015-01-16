# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0017_auto_20150116_1517'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryitem',
            name='replacement_cost_date',
            field=models.DateField(default=None, null=True, blank=True),
            preserve_default=True,
        ),
    ]
