# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-05-03 15:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0003_add_definition'),
    ]

    operations = [
        migrations.AddField(
            model_name='definition',
            name='slug',
            field=models.SlugField(max_length=500, null=True),
        ),
    ]
