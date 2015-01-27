# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('uw_inventory', '0056_inventoryitem_technician'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryitem',
            name='owner',
            field=models.ForeignKey(related_name=b'owners', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
