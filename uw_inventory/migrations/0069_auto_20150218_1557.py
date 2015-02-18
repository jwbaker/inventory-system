# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('uw_inventory', '0068_auto_20150217_1310'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('body', models.TextField(null=True, blank=True)),
                ('creation_date', models.DateTimeField(default=datetime.datetime.now)),
                ('title', models.CharField(max_length=255)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('inventory_item', models.ForeignKey(to='uw_inventory.InventoryItem')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='note',
            name='author',
        ),
        migrations.RemoveField(
            model_name='note',
            name='inventory_item',
        ),
        migrations.DeleteModel(
            name='Note',
        ),
    ]
