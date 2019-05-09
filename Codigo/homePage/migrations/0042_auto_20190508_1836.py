# Generated by Django 2.2 on 2019-05-08 23:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homePage', '0041_delete_aficion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='generoliterario',
            name='nombre',
        ),
        migrations.AddField(
            model_name='generoliterario',
            name='Ciencia_Ficción',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='generoliterario',
            name='Comedia',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='generoliterario',
            name='Drama',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='generoliterario',
            name='Terror',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='generoliterario',
            name='Tragicomedia',
            field=models.BooleanField(default=False),
        ),
        migrations.RemoveField(
            model_name='infolibro',
            name='genero',
        ),
        migrations.AddField(
            model_name='infolibro',
            name='genero',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='homePage.GeneroLiterario'),
        ),
    ]
