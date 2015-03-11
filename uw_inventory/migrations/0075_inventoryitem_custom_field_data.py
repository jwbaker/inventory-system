# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0074_itemfile_file_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryitem',
            name='custom_field_data',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
