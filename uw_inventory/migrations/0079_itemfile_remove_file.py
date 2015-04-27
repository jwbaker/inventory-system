# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0078_auto_20150420_1500'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemfile',
            name='remove_file',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
