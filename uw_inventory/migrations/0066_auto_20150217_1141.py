# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0065_itemfile_to_display'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='itemfile',
            options={'permissions': ('view_deleted_itemfile', 'Can view deleted item files')},
        ),
    ]
