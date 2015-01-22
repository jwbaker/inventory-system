# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0042_auto_20150122_0844'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='autocompletedata',
            unique_together=set([('name', 'kind')]),
        ),
    ]
