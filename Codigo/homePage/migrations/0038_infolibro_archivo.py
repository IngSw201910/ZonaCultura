# Generated by Django 2.2 on 2019-05-07 07:11

from django.db import migrations, models
import homePage.models


class Migration(migrations.Migration):

    dependencies = [
        ('homePage', '0037_remove_infolibro_archivo'),
    ]

    operations = [
        migrations.AddField(
            model_name='infolibro',
            name='archivo',
            field=models.FileField(default='contenido/books/default.pdf', upload_to='contenido/books/', validators=[homePage.models.validate_file_extension]),
        ),
    ]
