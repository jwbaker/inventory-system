# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0076_auto_20150323_1547'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('report_data', models.TextField()),
                ('owner', models.ForeignKey(default=None, blank=True, to='uw_inventory.InventoryItem', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
