# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-17 08:25
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0002_auto_20170717_0825'),
    ]

    operations = [
        migrations.AddField(
            model_name='bills',
            name='links',
            field=django.contrib.postgres.fields.jsonb.JSONField(null=True),
        ),
    ]