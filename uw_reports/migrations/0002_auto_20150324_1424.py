# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0076_auto_20150323_1547'),
        ('uw_reports', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='creation_date',
            field=models.DateField(default=datetime.datetime.now),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='report',
            name='creator',
            field=models.ForeignKey(related_name=b'creator', default=None, blank=True, to='uw_inventory.InventoryItem', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='report',
            name='owner',
            field=models.ForeignKey(related_name=b'report_owner', default=None, blank=True, to='uw_inventory.InventoryItem', null=True),
        ),
    ]
