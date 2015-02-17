# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0064_auto_20150213_1326'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemfile',
            name='to_display',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
