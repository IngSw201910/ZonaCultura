# Generated by Django 2.2 on 2019-04-16 21:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homePage', '0021_compradores_pagado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='compradores',
            name='pagado',
        ),
    ]