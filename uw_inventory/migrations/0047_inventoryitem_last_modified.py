# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0046_auto_20150122_1549'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryitem',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime.now, auto_now=True),
            preserve_default=True,
        ),
    ]
