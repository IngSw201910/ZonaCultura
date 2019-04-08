
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from homePage.models  import infousuario
from homePage.models  import infoLibro


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
 		 ]

 		labels={
 		 'aficiones':'Disciplinas',
 		   }
 		widgets={
 			#'aficiones':forms.CheckboxSelectMultiple(),
 			#'is_Creador_De_Contenido':forms.CheckBoxSelectMultiple
 		}
