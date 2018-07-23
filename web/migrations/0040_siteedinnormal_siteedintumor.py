# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0039_auto_20180711_1749'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteEdinNormal',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('edin5', models.PositiveIntegerField(default=0)),
                ('p50', models.DecimalField(max_digits=5, decimal_places=4)),
                ('cancer', models.ForeignKey(to='web.Cancer')),
                ('site', models.ForeignKey(to='web.Site')),
            ],
        ),
        migrations.CreateModel(
            name='SiteEdinTumor',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('edin5', models.PositiveIntegerField(default=0)),
                ('p50', models.DecimalField(max_digits=5, decimal_places=4)),
                ('cancer', models.ForeignKey(to='web.Cancer')),
                ('site', models.ForeignKey(to='web.Site')),
            ],
        ),
    ]
