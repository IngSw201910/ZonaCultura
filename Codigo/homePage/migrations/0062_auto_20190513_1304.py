# Generated by Django 2.2 on 2019-05-13 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homePage', '0061_auto_20190513_1301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contenidomanualidad',
            name='tipo',
            field=models.CharField(choices=[('escultura', 'escultura'), ('pintura', 'pintura')], max_length=9, null=True),
        ),
    ]