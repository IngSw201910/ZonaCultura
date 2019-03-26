from django.db import models

# Create your models here.
from multiselectfield import MultiSelectField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Aficion (models.Model):
	nombre= models.CharField(max_length=50)
	def __str__(self):
		return'{}'.format(self.nombre)
class infousuario(models.Model):
	user= models.OneToOneField (User,on_delete=models.CASCADE)
	aficiones= models.ManyToManyField(Aficion)
	es_CreadorDeContenido= models.BooleanField(default=False)
	es_Nada= models.BooleanField(default=False)
	def __str__(self):
		return'{}'.format(self.user.first_name + ' '+self.user.last_name)
	#is_Escritor= models.BooleanField (default=False)

