# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0012_auto_20150115_0859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventoryitem',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
