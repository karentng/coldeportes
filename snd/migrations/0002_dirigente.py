# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snd', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dirigente',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('cargo', models.CharField(max_length=100)),
                ('foto', models.ImageField(blank=True, null=True, upload_to='fotos')),
                ('superior', models.ForeignKey(to='snd.Dirigente')),
            ],
        ),
    ]
