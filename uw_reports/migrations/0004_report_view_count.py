# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_reports', '0003_auto_20150324_1602'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='view_count',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
    ]
