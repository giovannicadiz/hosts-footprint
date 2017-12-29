# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-28 13:14
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area', models.CharField(blank=True, max_length=255)),
                ('cargo', models.CharField(blank=True, max_length=255)),
                ('pais', models.CharField(blank=True, choices=[('ARGENTINA', 'ARGENTINA'), ('BRASIL', 'BRASIL'), ('CHILE', 'CHILE'), ('COLOMBIA', 'COLOMBIA'), ('PERU', 'PERU'), ('REGIONAL', 'REGIONAL'), ('SIN ASIGNAR', 'SIN ASIGNAR')], max_length=11)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]