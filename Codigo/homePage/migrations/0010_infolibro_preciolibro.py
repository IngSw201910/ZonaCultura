# Generated by Django 2.2 on 2019-04-14 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homePage', '0009_auto_20190413_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='infolibro',
            name='PrecioLibro',
            field=models.IntegerField(default=0),
        ),
    ]