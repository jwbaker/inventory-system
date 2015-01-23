# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0048_auto_20150122_1635'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryitem',
            name='tech_id',
            field=models.CharField(default=None, max_length=255, null=True, blank=True, validators=[django.core.validators.RegexValidator(b'[A-Z]{2}-[0-9]*', b'Must be of the form AA-0000')]),
            preserve_default=True,
        ),
    ]
