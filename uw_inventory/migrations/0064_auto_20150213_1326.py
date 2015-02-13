# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0063_auto_20150205_1257'),
    ]

    operations = [
        migrations.RenameField(
            model_name='itemfile',
            old_name='file',
            new_name='file_field',
        ),
        migrations.AddField(
            model_name='itemfile',
            name='mimetype',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
