# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('spike', '0002_datarecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='datarecord',
            name='data_src',
            field=models.CharField(max_length=30, default=datetime.datetime(2015, 12, 8, 21, 22, 3, 894955, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
