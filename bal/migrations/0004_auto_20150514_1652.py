# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bal', '0003_auto_20150514_1632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bal',
            name='agranulocytoza',
            field=models.NullBooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bal',
            name='alogenni_transplantace',
            field=models.NullBooleanField(default=False),
            preserve_default=True,
        ),
    ]
