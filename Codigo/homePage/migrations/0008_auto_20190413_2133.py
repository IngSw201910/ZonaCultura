# Generated by Django 2.2 on 2019-04-14 02:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homePage', '0007_auto_20190406_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infolibro',
            name='imagen',
            field=models.ImageField(blank=True, default='images/books/covers/default.jpg', null=True, upload_to='images/books/covers/'),
        ),
        migrations.CreateModel(
            name='Carrito',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libro', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='homePage.infoLibro')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='homePage.infousuario')),
            ],
        ),
    ]
