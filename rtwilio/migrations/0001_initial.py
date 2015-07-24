# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TwilioResponse',
            fields=[
                ('date', models.DateTimeField()),
                ('message', models.CharField(max_length=64, serialize=False, primary_key=True)),
                ('account', models.CharField(max_length=64)),
                ('sender', models.CharField(max_length=16)),
                ('recipient', models.CharField(max_length=16)),
                ('status', models.CharField(max_length=16)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
