# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0020_inventoryitem_factory_csa'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryitem',
            name='csa_special',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
