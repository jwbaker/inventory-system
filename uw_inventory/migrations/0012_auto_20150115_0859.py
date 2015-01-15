# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0011_auto_20150115_0855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventoryitem',
            name='creation_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
