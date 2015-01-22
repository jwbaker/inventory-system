# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0041_inventoryitem_lifting_device_inspection_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inventoryitem',
            old_name='csa_required',
            new_name='csa_not_required',
        ),
    ]
