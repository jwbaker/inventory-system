# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0067_auto_20150217_1141'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventoryitem',
            name='deleted',
        ),
        migrations.AddField(
            model_name='inventoryitem',
            name='to_display',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
