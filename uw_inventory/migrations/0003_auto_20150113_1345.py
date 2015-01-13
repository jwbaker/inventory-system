# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0002_auto_20150112_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventoryitem',
            name='status',
            field=models.CharField(blank=True, max_length=2, null=True, choices=[(b'SA', b'Stay'), (b'SO', b'Storage'), (b'SU', b'Surplussed'), (b'OT', b'Other')]),
        ),
    ]
