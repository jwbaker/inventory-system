# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0006_auto_20150114_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventoryitem',
            name='description',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='inventoryitem',
            name='name',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]
