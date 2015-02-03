# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0061_auto_20150203_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemfile',
            name='file',
            field=models.FileField(upload_to=b'files/'),
        ),
    ]
