# Generated by Django 2.2 on 2019-04-16 17:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homePage', '0018_articuloscomprados'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='carrito',
            unique_together={('libro', 'usuario')},
        ),
    ]