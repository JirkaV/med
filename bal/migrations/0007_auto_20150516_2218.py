# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('bal', '0006_auto_20150516_2217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pacient',
            name='datum_narozeni',
            field=models.DateField(default=datetime.date.today),
            preserve_default=True,
        ),
    ]
