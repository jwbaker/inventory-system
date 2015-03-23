# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw_inventory', '0075_inventoryitem_custom_field_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemfile',
            name='file_field',
            field=models.FileField(upload_to=b'media/files/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='itemimage',
            name='file_field',
            field=models.ImageField(upload_to=b'media/images/%Y/%m/%d/'),
        ),
    ]
