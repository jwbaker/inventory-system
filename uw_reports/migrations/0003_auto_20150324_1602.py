# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('uw_reports', '0002_auto_20150324_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='creator',
            field=models.ForeignKey(related_name=b'creator', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='owner',
            field=models.ForeignKey(related_name=b'owner', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
