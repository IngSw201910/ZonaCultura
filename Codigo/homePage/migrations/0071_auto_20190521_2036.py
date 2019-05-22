# Generated by Django 2.2 on 2019-05-22 01:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homePage', '0070_auto_20190521_1937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contenidomanualidad',
            name='precioV',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(50)]),
        ),
        migrations.AlterField(
            model_name='infolibro',
            name='PrecioLibro',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(50)]),
        ),
        migrations.AlterField(
            model_name='infousuario',
            name='balance',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(50)]),
        ),
    ]
