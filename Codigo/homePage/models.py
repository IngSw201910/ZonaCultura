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

class infoLibro(models.Model):
	user=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
	genero= models.ManyToManyField(GeneroLiterario)
	formato=models.ManyToManyField(FormatoLiterario)
	Titulo= models.CharField(max_length=50)
	Descripcion=models.TextField(max_length=2000)
	ISBN= models.IntegerField()
	PrecioLibro= models.IntegerField(default=0)
	CantidadPaginas=models.IntegerField()
	Idioma=models.CharField(max_length=15)
	imagen=models.ImageField(upload_to='images/books/covers/',default='images/books/covers/default.jpg', null=True,blank=True )
	def __str__(self):
		return'{}'.format(self.Titulo+' de '+self.user.first_name + ' '+self.user.last_name)
class infousuario(models.Model):
	balance= models.IntegerField(default=0)
	user= models.OneToOneField (User,on_delete=models.CASCADE)
	aficiones= models.ManyToManyField(Aficion, blank=True)
	es_CreadorDeContenido= models.BooleanField(default=False)
	es_Nada= models.BooleanField(default=False)
	def __str__(self):
		return'{}'.format(self.user.first_name + ' '+self.user.last_name)
	#is_Escritor= models.BooleanField (default=False)
class Carrito(models.Model):

		libro= models.ForeignKey(infoLibro, on_delete=models.SET_NULL,null=True)
		#multimedia
		#manualidad
		usuario=models.ForeignKey (infousuario,on_delete=models.SET_NULL, null=True)
		class Meta:
			unique_together=('libro', 'usuario')
class cuentaPorCobrar(models.Model):
	usuarioComprador= models.ForeignKey (infousuario,on_delete=models.SET_NULL, null=True, related_name='%(class)s_usuarioComprador')
	usuarioPropioDelCobro=models.ForeignKey (infousuario,on_delete=models.SET_NULL, null=True,related_name='%(class)s_usuarioPropioDelCobro')
	articuloLibro=models.ForeignKey(infoLibro, on_delete=models.SET_NULL,null=True)

class infoTarjeta(models.Model):
	numeroTarjeta= models.IntegerField()
	nombreTitular= models.CharField(max_length=15)
	apellidoTitular= models.CharField(max_length=15)
	fechaExpiración =models.CharField(max_length=5)
	codigoSeguridad= models.IntegerField()
	def __str__(self):
		return'{}'.format(self.numeroTarjeta + ' '+self.nombreTitular )

class PagoCreditoManager (models.Manager):
	def crear_pago (self,id_pago,usuario,balance):
		pago= self.Create(usuario= usuario,id_pago=id_pago,balance=balance)
		return pago
class PagoCredito (models.Model):
	usuario=models.ForeignKey (infousuario,on_delete=models.SET_NULL, null=True)
	id_pago=models.CharField(max_length=64, db_index=True)
	pagado=models.BooleanField(default=False)
	objects=PagoCreditoManager()
class ArticulosComprados(models.Model):
		libro = models.ForeignKey(infoLibro, on_delete=models.SET_NULL,null=True)
		#multimedia=NULL
		#manualidad=NULL
		usuario=models.ForeignKey (infousuario,on_delete=models.SET_NULL, null=True)
	


