# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0037_auto_20150121_1615'),
    ]

    operations = [
        migrations.CreateModel(
            name='AutocompleteData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('kind', models.CharField(max_length=255, choices=[(b'location', b'location'), (b'manufacturer', b'manufacturer')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='inventoryitem',
            name='location',
            field=models.ForeignKey(related_name=b'locations', default=None, blank=True, to='uw_inventory.AutocompleteData', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='inventoryitem',
            name='manufacturer',
            field=models.ForeignKey(related_name=b'manufacturers', default=None, blank=True, to='uw_inventory.AutocompleteData', null=True),
            preserve_default=True,
        ),
    ]
