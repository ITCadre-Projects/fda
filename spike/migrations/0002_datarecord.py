# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spike', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataRecord',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('captured_date', models.DateField()),
                ('raw_data', models.CharField(max_length=50000)),
                ('submitted_date', models.DateField()),
            ],
        ),
    ]
