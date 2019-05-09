# Generated by Django 2.2 on 2019-05-09 03:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homePage', '0042_auto_20190508_1836'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='generomanualidad',
            name='nombre',
        ),
        migrations.AddField(
            model_name='generomanualidad',
            name='Bodegon',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='generomanualidad',
            name='Desnudo',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='generomanualidad',
            name='Estatuilla',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='generomanualidad',
            name='Figura',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='generomanualidad',
            name='Funeraria',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='generomanualidad',
            name='Historico',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='generomanualidad',
            name='Mitologico',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='generomanualidad',
            name='Monumento',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='generomanualidad',
            name='Paisaje',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='generomanualidad',
            name='Relieve',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='generomanualidad',
            name='Religioso',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='generomanualidad',
            name='Retrato',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='generomanualidad',
            name='Terror',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='generomanualidad',
            name='Vanitas',
            field=models.BooleanField(default=False),
        ),
        migrations.RemoveField(
            model_name='contenidomanualidad',
            name='genero',
        ),
        migrations.AddField(
            model_name='contenidomanualidad',
            name='genero',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='homePage.GeneroManualidad'),
        ),
    ]
