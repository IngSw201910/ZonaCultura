# Generated by Django 2.2 on 2019-05-01 03:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('homePage', '0023_infousuario_profile_img'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeneroManualidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='contenidomultimedia',
            name='formato',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='contenidomultimedia',
            name='precioV',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='contenidoManualidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('descripcion', models.TextField(max_length=150)),
                ('precioV', models.IntegerField(default=0)),
                ('imagen', models.ImageField(blank=True, default='images/manualidades/covers/default.jpg', null=True, upload_to='images/manualidades/covers/')),
                ('genero', models.ManyToManyField(to='homePage.GeneroManualidad')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
