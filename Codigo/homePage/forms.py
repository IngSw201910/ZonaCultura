
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from homePage.models  import infousuario
from homePage.models  import infoLibro
from homePage.models import infoTarjeta
from homePage.models import contenidoMultimedia
from homePage.models import Donacion
from homePage.models import contenidoManualidad
from homePage.models import Comentario
from homePage.models import competencias
from homePage.models import GeneroLiterario
from homePage.models import GeneroManualidad
from homePage.models import BusquedaString
from homePage.models import Mensajes
from homePage.models import Contrato
from homePage.models import ComentarioObraLiteraria
from django.forms import ModelForm



class logInForm (forms.Form):
	nombreUsuario=forms.CharField(max_length=150, required=True, label ="Nombre de Usuario",widget=(forms.TextInput()))
	contraseniaUsuario= forms.CharField(max_length=150, required=True, label= "Contraseña",widget=(forms.PasswordInput()))
class generoLiterarioForm(forms.ModelForm):
	class Meta:
		model=GeneroLiterario
		fields=[
		'Comedia',
		'Drama',
		'Tragicomedia',
		'Terror',
		'Ciencia_Ficción' ,
		]
class RegistroForm(UserCreationForm):
	class Meta:
		model= User
		fields=[
		'username',
		'first_name',
		'last_name',
		'email',
		]
		labels={
		'username':'Nombre de Usuario',
		'first_name':'Nombres',
		'last_name': 'Apellidos',
		'email':'Correo electronico',
		}
class MensajeForm (forms.ModelForm):
	class Meta:
		model=Mensajes
		fields=[
		'Titulo',
		'Cuerpo',
		]
		labels={
		'Titulo':'Digitar Titulo del Mensaje',
		'Cuerpo': 'Digitar Cuerpo del Mensaje',
		}
class ContratoForm (forms.ModelForm):
	class Meta:
		model=Contrato
		fields=[
		'Titulo',
		'Cuerpo',
		'valorOfrecido'
		]
		labels={
		'Titulo':'Digitar Titulo del Contrato',
		'Cuerpo': 'Digitar Cuerpo del Contrato',
		'valorOfrecido': 'Digitar cuánto va a ofrecer por el contrato'
		}
class competenciasForm(forms.ModelForm):
	class Meta:
		model=competencias
		fields=[
		'Escritor',
		'Pintor',
		'Escultor',
		'Cantante',
		'Guitarrista',
		'Bajista',
		'Pianista',
		'Baterista',
		'Violinista',
		'Saxofonista',
		'Acordeonista',
		'Trompetista',
		'Fotografo',
		'Actor',
		]
class GeneroManualidadForm(forms.ModelForm):
	class Meta:
		model=GeneroManualidad
		fields=[
		'Bodegon',
		'Vanitas',
		'Retrato',
		'Terror',
	    'Desnudo',
	    'Religioso',
	    'Historico',
	    'Mitologico',
	    'Paisaje',
	    'Funeraria',
	    'Retrato',
	    'Monumento',
	    'Estatuilla',
	    'Figura',
	    'Relieve'
		]
class contenidoLiterarioForm(forms.ModelForm):
	class Meta:
		model=infoLibro
		fields=[
		'Titulo',
		'imagen',
		'archivo',
		'Descripcion',
		'ISBN',
		'CantidadPaginas',
		'Idioma'
		]
		labels={
		'archivo':'Archivo del contenido literario (Solo acepta formato pdf)',
		'Titulo':'Titulo',
		'imagen':'Imagen del contenido literario',
		'Descripcion':'Descripcion',
		'ISBN':'Numero ISBN',
		'CantidadPaginas':'Numero de paginas del producto',
		'Idioma':'Idioma en el que esta escrito el contenido literario'
		}
		widgets={
 			#'formato':forms.CheckboxSelectMultiple(),
 			#'genero': forms.CheckboxSelectMultiple(),
 			#'is_Creador_De_Contenido':forms.CheckBoxSelectMultiple
 		}
class BusquedaStringForm(forms.ModelForm):
	class Meta:
		model=infoLibro
		fields=[
		'Titulo',
		'imagen',
		'archivo',
		'Descripcion',
		'ISBN',
		'CantidadPaginas',
		'Idioma'
		]
		labels={
		'archivo':'Archivo del contenido literario (Solo acepta formato pdf)',
		'Titulo':'Titulo',
		'imagen':'Imagen del contenido literario',
		'Descripcion':'Descripcion',
		'ISBN':'Numero ISBN',
		'CantidadPaginas':'Numero de paginas del producto',
		'Idioma':'Idioma en el que esta escrito el contenido literario'
		}
		widgets={
 			#'formato':forms.CheckboxSelectMultiple(),
 			#'genero': forms.CheckboxSelectMultiple(),
 			#'is_Creador_De_Contenido':forms.CheckBoxSelectMultiple
 		}

class infoForm(forms.ModelForm):
 	class Meta:
 		model=infousuario
 		fields=[
 		'es_CreadorDeContenido',
 		'profile_img'
 		 ]

 		labels={
 		'es_CreadorDeContenido' : 'Quiere ser creador de contenido',
 		'profile_img': 'Imagen de Perfil'
 		   }
 		widgets={

 		}
class contenidoTarjetaForm(forms.ModelForm):
	class Meta:
		model=infoTarjeta
		fields=[
		'numeroTarjeta',
		'nombreTitular',
		'apellidoTitular',
		'mesExpiracion',
		'anoExpiracion',
		'codigoSeguridad'
		]
		labels={
		'numeroTarjeta':'Número de la tarjeta de credito',
		'nombreTitular':'Nombre del titular',
		'apellidoTitular':'Apellido del titulat',
		'mesExpiracion':'Mes de expiración Formato mm',
		'anoExpiracion':'Ano de expiración Formato aa',
		'codigoSeguridad':'Código de seguridad de la tarjeta'
		}
		widgets={
		'numeroTarjeta': forms.TextInput(attrs={'class':'form-control'}),
		'nombreTitular':forms.TextInput(attrs={'class':'form-control'}),
		'apellidoTitular':forms.TextInput(attrs={'class':'form-control'}),
		'mesExpiracion':forms.TextInput(attrs={'class':'form-control'}),
		'anoExpiracion':forms.TextInput(attrs={'class':'form-control'}),
		'codigoSeguridad':forms.TextInput(attrs={'class':'form-control'}),
		}
class contenidoCreditForm(forms.ModelForm):
	class Meta:
		model=infousuario
		fields=[
		'balance'
		]
		labels={
		'balance':'ingrese el credito'
		}
		widgets={
		'balance': forms.TextInput(attrs={'class':'form-control'}),
 			#'formato':forms.CheckboxSelectMultiple(),
 			#'genero': forms.CheckboxSelectMultiple(),
 			#'is_Creador_De_Contenido':forms.CheckBoxSelectMultiple
 		}
class contenidoMultimediaForm(ModelForm):
	class Meta:
		model=contenidoMultimedia
		fields= [
		'user',
		'title',
		'descripcion',
		'formato',
		'precioV',
		'clip',
		'fecha',
		]
		labels={
		'user': 'Nombre del Autor',
		'title': 'Titulo del Video',
		'descripcion':'Descripcion del Video',
		'formato':'Formato del Video',
		'precioV':'Precio del Video',
		'clip':'Contenido Multimedia',
		'fecha': 'Fecha de Creacion',
		}
		widgets={
 			#'formato':forms.CheckboxSelectMultiple(),
 			#'genero': forms.CheckboxSelectMultiple(),
 			#'is_Creador_De_Contenido':forms.CheckBoxSelectMultiple
 		}
class DonacionForm(ModelForm):
	class Meta:
		model=Donacion
		fields= [
		'cantidad',
		'mensaje'
		]
		labels={
		'cantidad': 'Valor de la donacion',
		'mensaje':'Mensaje para el usuario a donar'
		}
		widgets={
 			#'formato':forms.CheckboxSelectMultiple(),
 			#'genero': forms.CheckboxSelectMultiple(),
 			#'is_Creador_De_Contenido':forms.CheckBoxSelectMultiple
 		}

class contenidoManualForm(forms.ModelForm):
	class Meta:
		model=contenidoManualidad
		fields=[
		'title',
		'existencias',
		'descripcion',
		'precioV',
		'imagen',
		'imagen2',
		'imagen3',
		'tipo'

		]
		labels={
		'title':'Titulo',
		'existencias':'Existencias',
		'descripcion':'Descripcion',
		'precioV':'Precio de la manualidad',
		'imagen':'Imagen del contenido manual',
		'imagen2':'Imagen del contenido manual',
		'imagen3':'Imagen del contenido manual',
		'tipo':'Tipo de manualidad'
		}


class comenycaliForm(ModelForm):
	class Meta:
		model=Comentario
		fields= [
		'califi',
		'comentario'
		]
		labels={
		'califi': 'Puntaje de 1-5',
		'comentario':'Comentarios acerca de la obra'
		}
		widgets={
 			#'formato':forms.CheckboxSelectMultiple(),
 			#'genero': forms.CheckboxSelectMultiple(),
 			#'is_Creador_De_Contenido':forms.CheckBoxSelectMultiple
 		}
class comenycaliFormLibro(ModelForm):
	class Meta:
		model=ComentarioObraLiteraria
		fields= [
		'califi',
		'comentario'
		]
		labels={
		'califi': 'Puntaje de 1-5',
		'comentario':'Comentarios acerca de la obra'
		}
		widgets={
 			#'formato':forms.CheckboxSelectMultiple(),
 			#'genero': forms.CheckboxSelectMultiple(),
 			#'is_Creador_De_Contenido':forms.CheckBoxSelectMultiple
 		}
class BusquedaStringForm(forms.ModelForm):
	class Meta:
		model=BusquedaString
		fields=[
		'generoBusqueda'

		]
		labels={
		'generoBusqueda': 'Buscar'
		}
