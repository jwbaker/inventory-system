# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0054_auto_20150126_1534'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryitem',
            name='supplier',
            field=models.ForeignKey(related_name=b'suppliers', default=None, blank=True, to='uw_inventory.AutocompleteData', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='autocompletedata',
            name='kind',
            field=models.CharField(max_length=255, choices=[(b'location', b'location'), (b'manufacturer', b'manufacturer'), (b'supplier', b'supplier')]),
        ),
    ]
