# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-08 06:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0002_auto_20170707_1519'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='hangout_link',
            field=models.URLField(blank=True, null=True),
        ),
    ]