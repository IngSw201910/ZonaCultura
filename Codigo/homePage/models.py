from django.db import models

# Create your models here.

from multiselectfield import MultiSelectField

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import ModelForm
from django.utils import timezone
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
def validate_file_extension(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError('Error message')
class Mensajes (models.Model):
	Emisor=models.ForeignKey(User,on_delete=models.SET_NULL, null=True, related_name='%(class)s_Emisor')
	Receptor=models.ForeignKey(User,on_delete=models.SET_NULL, null=True, related_name='%(class)s_Pasivo')
	Titulo=models.CharField(max_length=50)
	Cuerpo=models.TextField(max_length=150)
	fecha=models.DateTimeField(default=timezone.now)
class Contactos(models.Model):
	Activo=models.ForeignKey(User,on_delete=models.SET_NULL, null=True, related_name='%(class)s_Activo')
	Pasivo=models.ForeignKey(User,on_delete=models.SET_NULL, null=True,  related_name='%(class)s_Pasivo')
class competencias (models.Model):
	Escritor=models.BooleanField(default=False)
	Pintor=models.BooleanField(default=False)
	Escultor=models.BooleanField(default=False)
	Cantante=models.BooleanField(default=False)
	Guitarrista=models.BooleanField(default=False)
	Bajista=models.BooleanField(default=False)
	Pianista=models.BooleanField(default=False)
	Baterista=models.BooleanField(default=False)
	Violinista=models.BooleanField(default=False)
	Saxofonista=models.BooleanField(default=False)
	Acordeonista=models.BooleanField(default=False)
	Trompetista=models.BooleanField(default=False)
	Fotografo=models.BooleanField(default=False)
	Actor=models.BooleanField(default=False)
class FormatoLiterario(models.Model):
	nombre=models.CharField(max_length=50)
	def __str__(self):
		return'{}'.format(self.nombre)

class GeneroMultimedia(models.Model):
	Comedia=models.BooleanField(default=False)
	Drama=models.BooleanField(default=False)
	Retrato=models.BooleanField(default=False)
	Terror=models.BooleanField(default=False)
	Accion=models.BooleanField(default=False)
	Belico=models.BooleanField(default=False)
	CienciaFiccion =models.BooleanField(default=False)
	Aventura =models.BooleanField(default=False)
	DelOeste=models.BooleanField(default=False)
	ArtesMarciales=models.BooleanField(default=False)
	Fantastico=models.BooleanField(default=False)
	Suspenso=models.BooleanField(default=False)
	Historico =models.BooleanField(default=False)
	Adolescente =models.BooleanField(default=False)
	Infantil =models.BooleanField(default=False)
	Político_Social=models.BooleanField(default=False)
	Animacion=models.BooleanField(default=False)

class GeneroLiterario(models.Model):
	Comedia=models.BooleanField(default=False)
	Drama=models.BooleanField(default=False)
	Tragicomedia=models.BooleanField(default=False)
	Terror=models.BooleanField(default=False)
	Ciencia_Ficción =models.BooleanField(default=False)

class GeneroManualidad(models.Model):
	Bodegon=models.BooleanField(default=False)
	Vanitas=models.BooleanField(default=False)
	Retrato=models.BooleanField(default=False)
	Terror=models.BooleanField(default=False)
	Desnudo=models.BooleanField(default=False)
	Religioso=models.BooleanField(default=False)
	Historico=models.BooleanField(default=False)
	Mitologico =models.BooleanField(default=False)
	Paisaje=models.BooleanField(default=False)
	Funeraria=models.BooleanField(default=False)
	Retrato=models.BooleanField(default=False)
	Monumento=models.BooleanField(default=False)
	Estatuilla =models.BooleanField(default=False)
	Figura =models.BooleanField(default=False)
	Relieve =models.BooleanField(default=False)

class contenidoManualidad(models.Model):
	user=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
	title=models.CharField(max_length=50)
	existencias=models.IntegerField(default=0)
	descripcion=models.TextField(max_length=150)
	genero=models.ForeignKey(GeneroManualidad, on_delete=models.SET_NULL, null=True)
	precioV=models.PositiveIntegerField(default=0)
	imagen=models.ImageField(upload_to='images/manualidades/covers/',default='images/manualidades/covers/default.jpg', null=True,blank=True )
	imagen2=models.ImageField(upload_to='images/manualidades/covers/',default='images/manualidades/covers/default.jpg', null=True,blank=True )
	imagen3=models.ImageField(upload_to='images/manualidades/covers/',default='images/manualidades/covers/default.jpg', null=True,blank=True )
	puntaje=models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, default=0.00)
	canticomp=models.IntegerField(default=0)
	escultura='escultura'
	pintura='pintura'
	TipoMan= (
        (escultura, 'escultura'),
        (pintura, 'pintura'),
        
    )
	tipo=models.CharField(max_length=9,choices=TipoMan, null=True)
	def __str__(self):
		return'{}'.format(self.title)
class infoLibro(models.Model):
	user=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
	archivo=models.FileField(upload_to='contenido/books/', validators=[validate_file_extension],default='contenido/books/default.pdf')
	genero= models.ForeignKey(GeneroLiterario, on_delete=models.SET_NULL, null=True)
	Titulo= models.CharField(max_length=50)
	Descripcion=models.TextField(max_length=2000)
	ISBN= models.IntegerField()
	PrecioLibro= models.IntegerField(default=0)
	CantidadPaginas=models.IntegerField()
	Idioma=models.CharField(max_length=15)
	imagen=models.ImageField(upload_to='images/books/covers/',default='images/books/covers/default.jpg', null=True,blank=True )
	def __str__(self):
		return'{}'.format(self.Titulo)
class infousuario(models.Model):
	balance= models.IntegerField(default=0)
	user= models.OneToOneField (User,on_delete=models.CASCADE)
	aficiones= models.ForeignKey(competencias,on_delete=models.CASCADE,null=True)
	es_CreadorDeContenido= models.BooleanField(default=False)
	profile_img=models.ImageField(upload_to='images/profile/',default='images/profile/perfilb.jpg',null=False,blank=False)
	es_Nada= models.BooleanField(default=False)

	def __str__(self):
		return'{}'.format(self.user.first_name + ' '+self.user.last_name)
	#is_Escritor= models.BooleanField (default=False)
class Carrito(models.Model):
		libro= models.ForeignKey(infoLibro, on_delete=models.SET_NULL,null=True)
		manualidad= models.ForeignKey(contenidoManualidad, on_delete=models.SET_NULL,null=True)
		#multimedia
		usuario=models.ForeignKey (infousuario,on_delete=models.SET_NULL, null=True)
		class Meta:
			unique_together=('libro', 'usuario')
class cuentaPorCobrar(models.Model):
	usuarioComprador= models.ForeignKey (infousuario,on_delete=models.SET_NULL, null=True, related_name='%(class)s_usuarioComprador')
	usuarioPropioDelCobro=models.ForeignKey (infousuario,on_delete=models.SET_NULL, null=True,related_name='%(class)s_usuarioPropioDelCobro')
	articuloLibro=models.ForeignKey(infoLibro, on_delete=models.SET_NULL,null=True)
	articuloManual=models.ForeignKey(contenidoManualidad, on_delete=models.SET_NULL,null=True)

class infoTarjeta(models.Model):
	numeroTarjeta= models.PositiveIntegerField(validators=[MinValueValidator(1000000000000000),MaxValueValidator(9000000000000000)])
	nombreTitular= models.CharField(max_length=20)
	apellidoTitular= models.CharField(max_length=20)
	mesExpiracion =models.PositiveIntegerField(default=0,validators=[ MinValueValidator(1),MaxValueValidator(12)])
	anoExpiracion =models.PositiveIntegerField(default=0,validators=[MinValueValidator(19),MaxValueValidator(50)])
	codigoSeguridad= models.PositiveIntegerField(validators=[MaxValueValidator(900)])
	def __str__(self):
		return'{}'.format(self.nombreTitular )

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
		manualidad = models.ForeignKey(contenidoManualidad, on_delete=models.SET_NULL,null=True)
		#multimedia=NULL
		usuario=models.ForeignKey (infousuario,on_delete=models.SET_NULL, null=True)

class Compradores(models.Model):
		libro = models.ForeignKey(infoLibro, on_delete=models.SET_NULL,null=True)
		manualidad = models.ForeignKey(contenidoManualidad, on_delete=models.SET_NULL,null=True)
		usuarioDuenio=models.ForeignKey (infousuario,on_delete=models.SET_NULL, null=True,related_name='usuarioDuenio')
		usuarioComprador=models.ForeignKey (infousuario,on_delete=models.SET_NULL, null=True,related_name='usuarioComprador')

class contenidoMultimedia(models.Model):
	user=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
	title=models.CharField(max_length=50)
	descripcion=models.TextField(max_length=150)
	formato=models.CharField(max_length=20,blank=True)
	precioV=models.IntegerField(default=0)
	clip=models.FileField(upload_to='media/video')
	fecha=models.DateTimeField(default=timezone.now)
	genero=models.ForeignKey(GeneroMultimedia, on_delete=models.SET_NULL, null=True)

class Donacion(models.Model):
		usuarioDonante=models.ForeignKey (infousuario,on_delete=models.SET_NULL, null=True,related_name='usuarioDonante')
		usuarioBen=models.ForeignKey (infousuario,on_delete=models.SET_NULL, null=True,related_name='usuarioBen')
		cantidad =models.PositiveIntegerField(default=0)
		mensaje=models.TextField(max_length=150,default="")

class ComentarioObraLiteraria(models.Model):
	libro = models.ForeignKey(infoLibro, on_delete=models.SET_NULL,null=True)
	califi=models.PositiveIntegerField(default=0)
	comentario=models.TextField(max_length=150,default="")
	usuarioComentador=models.ForeignKey (infousuario,on_delete=models.SET_NULL, null=True)

class Comentario(models.Model):
		manu = models.ForeignKey(contenidoManualidad, on_delete=models.SET_NULL,null=True)
		califi=models.PositiveIntegerField(default=0)
		comentario=models.TextField(max_length=150,default="")
		usuarioComentador=models.ForeignKey (infousuario,on_delete=models.SET_NULL, null=True)

class BusquedaString (models.Model):
		generoBusqueda=models.CharField(max_length=30,blank=True)
		usuarioBuscador=models.ForeignKey (infousuario,on_delete=models.SET_NULL, null=True)
