# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_reports', '0005_auto_20150401_1105'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='report',
            options={'permissions': (('view_all_reports', 'Can view all reports'), ('view_deleted_report', 'Can view deleted reports'))},
        ),
        migrations.AddField(
            model_name='report',
            name='to_display',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
