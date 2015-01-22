# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0045_inventoryitem_sop_required'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventoryitem',
            name='sop_required',
            field=models.BooleanField(default=True),
        ),
    ]
