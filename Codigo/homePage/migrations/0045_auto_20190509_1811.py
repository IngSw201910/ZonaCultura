# Generated by Django 2.2 on 2019-05-09 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homePage', '0044_auto_20190508_2231'),
    ]

    operations = [
        migrations.AddField(
            model_name='contenidomanualidad',
            name='imagen2',
            field=models.ImageField(blank=True, default='images/manualidades/covers/default.jpg', null=True, upload_to='images/manualidades/covers/'),
        ),
        migrations.AddField(
            model_name='contenidomanualidad',
            name='imagen3',
            field=models.ImageField(blank=True, default='images/manualidades/covers/default.jpg', null=True, upload_to='images/manualidades/covers/'),
        ),
    ]