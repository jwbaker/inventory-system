# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0025_inventoryitem_csa_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryitem',
            name='lifting_device',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
