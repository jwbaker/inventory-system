# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0022_inventoryitem_csa_special_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryitem',
            name='modified_since_csa',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
