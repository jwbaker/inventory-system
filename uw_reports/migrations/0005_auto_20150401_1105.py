# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_reports', '0004_report_view_count'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='report',
            options={'permissions': (('view_all_reports', 'Can view all reports'),)},
        ),
    ]
