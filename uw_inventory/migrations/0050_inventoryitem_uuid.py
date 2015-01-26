# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0049_inventoryitem_tech_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryitem',
            name='uuid',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
