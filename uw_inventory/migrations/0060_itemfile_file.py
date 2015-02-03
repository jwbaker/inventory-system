# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0059_auto_20150203_0922'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemfile',
            name='file',
            field=models.FileField(default=None, upload_to=b''),
            preserve_default=False,
        ),
    ]
