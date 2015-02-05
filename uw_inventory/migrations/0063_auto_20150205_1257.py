# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0062_auto_20150203_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemfile',
            name='file',
            field=models.FileField(upload_to=b'files/%Y/%m/%d/'),
        ),
    ]
