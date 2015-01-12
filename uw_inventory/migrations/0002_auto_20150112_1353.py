# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventoryitem',
            name='status',
            field=models.CharField(default=None, max_length=2, null=True, blank=True, choices=[(b'SA', b'Stay'), (b'SO', b'Storage'), (b'SU', b'Surplussed'), (b'OT', b'Other')]),
        ),
    ]
