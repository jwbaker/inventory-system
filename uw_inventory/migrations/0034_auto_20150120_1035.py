# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0033_auto_20150120_0944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventoryitem',
            name='location',
            field=models.IntegerField(default=None, null=True, blank=True),
        ),
    ]
