# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0073_auto_20150225_0913'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemfile',
            name='file_type',
            field=models.CharField(default='other', max_length=255, choices=[(b'other', b'Other'), (b'manual', b'Manual')]),
            preserve_default=False,
        ),
    ]
