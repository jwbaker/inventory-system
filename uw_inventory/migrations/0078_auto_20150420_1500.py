# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0077_inventoryitem_qr_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemfile',
            name='file_type',
            field=models.CharField(default=b'other', max_length=255, null=True, blank=True, choices=[(b'other', b'Other'), (b'manual', b'Manual')]),
        ),
    ]
