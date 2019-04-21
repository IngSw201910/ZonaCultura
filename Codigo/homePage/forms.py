
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from homePage.models  import infousuario
from homePage.models  import infoLibro
from homePage.models import infoTarjeta
from homePage.models import contenidoMultimedia
from homePage.models import Donacion
from django.forms import ModelForm


class logInForm (forms.Form):
	nombreUsuario=forms.CharField(max_length=150, required=True, label ="Nombre de Usuario",widget=(forms.TextInput()))
	contraseniaUsuario= forms.CharField(max_length=150, required=True, label= "Contraseña",widget=(forms.PasswordInput()))

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

class contenidoLiterarioForm(forms.ModelForm):
	class Meta:
		model=infoLibro
		fields=[
		'Titulo',
		'imagen',
		'Descripcion',
		'ISBN',
		'CantidadPaginas',
		'formato',
		'genero',
		'Idioma'
		]
		labels={
		'Titulo':'Titulo',
		'imagen':'Imagen del contenido literario',
		'Descripcion':'Descripcion',
		'ISBN':'Numero ISBN',
		'CantidadPaginas':'Numero de paginas del producto',
		'formato':'Formato del contenido literario',
		'genero': 'Genero del contenido literario',
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
 		'aficiones',
 		'es_CreadorDeContenido',
 		'profile_img' 		
 		 ]

 		labels={
 		'aficiones': 'Posee algun taleno',
 		'es_CreadorDeContenido' : 'Quiere ser creador de contenido',
 		'profile_img': 'Imagen de Perfil' 	
 		   }
 		widgets={
 		'aficiones':forms.CheckboxSelectMultiple(),
 	    
 		}
class contenidoTarjetaForm(forms.ModelForm):
	class Meta:
		model=infoTarjeta
		fields=[
		'numeroTarjeta',
		'nombreTitular',
		'apellidoTitular',
		'fechaExpiración',
		'codigoSeguridad'
		]
		labels={
		'numeroTarjeta':'Número de la tarjeta de credito',
		'nombreTitular':'Nombre del titular',
		'apellidoTitular':'Apellido del titulat',
		'fechaExpiración':'Fecha de expiración Formato mm/aa',
		'codigoSeguridad':'Código de seguridad de la tarjeta'
		}
		widgets={
 			#'formato':forms.CheckboxSelectMultiple(),
 			#'genero': forms.CheckboxSelectMultiple(),
 			#'is_Creador_De_Contenido':forms.CheckBoxSelectMultiple
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
		'cantidad'
		]
		labels={
		'cantidad': 'Valor de la donacion'
		}
		widgets={
 			#'formato':forms.CheckboxSelectMultiple(),
 			#'genero': forms.CheckboxSelectMultiple(),
 			#'is_Creador_De_Contenido':forms.CheckBoxSelectMultiple
 		}