# Generated by Django 2.2 on 2019-05-08 23:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homePage', '0039_competencias'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='infousuario',
            name='aficiones',
        ),
        migrations.AddField(
            model_name='infousuario',
            name='aficiones',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='homePage.competencias'),
        ),
    ]