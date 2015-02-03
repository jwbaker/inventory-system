# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0058_note'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('inventory_item', models.ForeignKey(default=None, blank=True, to='uw_inventory.InventoryItem', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='inventoryitem',
            name='sop_file',
            field=models.ForeignKey(default=None, blank=True, to='uw_inventory.ItemFile', null=True),
            preserve_default=True,
        ),
    ]
