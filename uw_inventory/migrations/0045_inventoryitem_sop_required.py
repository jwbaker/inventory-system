# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0044_auto_20150122_1546'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryitem',
            name='sop_required',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
