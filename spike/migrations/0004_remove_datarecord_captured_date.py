# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spike', '0003_datarecord_data_src'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datarecord',
            name='captured_date',
        ),
    ]
