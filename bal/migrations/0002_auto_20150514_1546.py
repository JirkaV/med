# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diagnoza',
            name='kod',
            field=models.CharField(max_length=128),
            preserve_default=True,
        ),
    ]
