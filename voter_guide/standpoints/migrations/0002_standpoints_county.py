# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-30 10:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('standpoints', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='standpoints',
            name='county',
            field=models.CharField(default='\u81fa\u5317\u5e02', max_length=100),
            preserve_default=False,
        ),
    ]
