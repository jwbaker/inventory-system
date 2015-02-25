# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0071_inventoryitem_notes'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('file_field', models.ImageField(upload_to=b'images/%Y/%m/%d/')),
                ('to_display', models.BooleanField(default=True)),
                ('inventory_item', models.ForeignKey(default=None, blank=True, to='uw_inventory.InventoryItem', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
