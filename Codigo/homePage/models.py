from django.db import models

# Create your models here.
from multiselectfield import MultiSelectField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class FormatoLiterario(models.Model):
	nombre=models.CharField(max_length=50)
	def __str__(self):
		return'{}'.format(self.nombre)

class GeneroLiterario(models.Model):
	nombre=models.CharField(max_length=50)
	def __str__(self):
		return'{}'.format(self.nombre)

class Aficion (models.Model):
	nombre= models.CharField(max_length=50)
	def __str__(self):
		return'{}'.format(self.nombre)
class infousuario(models.Model):
	user= models.OneToOneField (User,on_delete=models.CASCADE)
	aficiones= models.ManyToManyField(Aficion, blank=True)
	es_CreadorDeContenido= models.BooleanField(default=False)
	es_Nada= models.BooleanField(default=False)
	def __str__(self):
		return'{}'.format(self.user.first_name + ' '+self.user.last_name)
	#is_Escritor= models.BooleanField (default=False)

class infoLibro(models.Model):
	user=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
	genero= models.ManyToManyField(GeneroLiterario)
	formato=models.ManyToManyField(FormatoLiterario)
	Titulo= models.CharField(max_length=50)
	Descripcion=models.TextField(max_length=2000)
	ISBN= models.IntegerField()
	CantidadPaginas=models.IntegerField()
	Idioma=models.CharField(max_length=15)
	imagen=models.ImageField(upload_to='images/books/covers/',default='images/books/covers/default.jpg', null=True,blank=True )
