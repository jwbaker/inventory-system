# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InventoryItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, blank=True)),
                ('creation_date', models.DateField(default=datetime.date.today, null=True, blank=True)),
                ('description', models.TextField(blank=True)),
                ('status', models.CharField(default=None, max_length=2, blank=True, choices=[(b'SA', b'Stay'), (b'SO', b'Storage'), (b'SU', b'Surplussed'), (b'OT', b'Other')])),
                ('purchase_price', models.IntegerField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
