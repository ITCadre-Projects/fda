# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataPoint',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('filed_date', models.DateField()),
                ('drug_name', models.CharField(max_length=200)),
                ('count', models.IntegerField(default=0)),
            ],
        ),
    ]
