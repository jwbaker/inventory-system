# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0021_inventoryitem_csa_special'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryitem',
            name='csa_special_date',
            field=models.DateField(default=None, null=True, blank=True),
            preserve_default=True,
        ),
    ]
