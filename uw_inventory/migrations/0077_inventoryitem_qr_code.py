# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0076_auto_20150323_1547'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryitem',
            name='qr_code',
            field=models.ImageField(default=None, null=True, upload_to=b'media/images/%Y/%m/%d/', blank=True),
            preserve_default=True,
        ),
    ]
