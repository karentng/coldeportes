# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tenant_schemas.postgresql_backend.base


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entidad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('domain_url', models.CharField(unique=True, max_length=128)),
                ('schema_name', models.CharField(validators=[tenant_schemas.postgresql_backend.base._check_schema_name], unique=True, max_length=63)),
                ('nombre', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
