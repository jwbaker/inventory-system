# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0024_inventoryitem_undergraduate'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryitem',
            name='csa_cost',
            field=models.IntegerField(default=None, null=True, blank=True),
            preserve_default=True,
        ),
    ]
