# Generated by Django 2.1.8 on 2019-04-18 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homePage', '0022_donacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='infousuario',
            name='profile_img',
            field=models.ImageField(default='images/profile/perfilb.jpg', upload_to='images/profile/'),
        ),
    ]
