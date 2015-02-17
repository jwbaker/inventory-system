# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0066_auto_20150217_1141'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='itemfile',
            options={'permissions': (('view_deleted_itemfile', 'Can view deleted item files'),)},
        ),
    ]
