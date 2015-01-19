# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0019_inventoryitem_csa_required'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryitem',
            name='factory_csa',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
