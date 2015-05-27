# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bal', '0004_auto_20150514_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agens',
            name='jmeno',
            field=models.CharField(max_length=200),
            preserve_default=True,
        ),
    ]
