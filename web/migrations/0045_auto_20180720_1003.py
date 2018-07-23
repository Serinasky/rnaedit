# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0044_auto_20180720_1002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteedincancer',
            name='edin5p',
            field=models.DecimalField(max_digits=4, decimal_places=1),
        ),
        migrations.AlterField(
            model_name='siteedincancer',
            name='p50p',
            field=models.DecimalField(max_digits=5, decimal_places=1),
        ),
    ]
