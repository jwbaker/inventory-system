# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0072_itemimage'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='itemimage',
            options={'permissions': (('view_deleted_itemimage', 'Can view deleted item images'),)},
        ),
    ]
