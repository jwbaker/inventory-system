# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0013_auto_20150115_1304'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryitem',
            name='deleted',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
