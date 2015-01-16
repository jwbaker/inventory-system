# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0018_inventoryitem_replacement_cost_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryitem',
            name='csa_required',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
