# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0028_auto_20150119_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventoryitem',
            name='creation_date',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]
