from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from homePage.forms import infoForm
from homePage.forms import RegistroForm
from homePage.forms import logInForm
from django.contrib.auth import authenticate, login
#from django.core.urlresolvers import reverse_lazy
def index(request):
	form=logInForm(request.POST or None)
	print("Inicio de sesion:")
	if form.is_valid():
		print("Forma valida:")
		data= form.cleaned_data
		nombreUsuario=data.get("nombreUsuario")
		Contrasenia= data.get("contraseniaUsuario")
		print("\n")
		print(nombreUsuario)
		print(Contrasenia)
		acceso= authenticate(username=nombreUsuario, password=Contrasenia)
		if acceso is not None:
			login(request,acceso)
			return HttpResponse("Bienvenido cliente")#TODO: return pagina de inicio despues de iniciar sesion
		else:
			return HttpResponse("Usuario o contraseña no coincide/existe")
	else:
		form=logInForm()
	return render(request, 'paginaInicio.html',{'form':form})
# Create your views here.

def registro(request):
	return render (request, 'Registro.html')

def registro_view(request):
	if request.method =='POST':
		User_Form= RegistroForm(request.POST)
		Info_Form=infoForm(request.POST)
		if User_Form.is_valid() and Info_Form.is_valid():
			user=User_Form.save()
			profile=Info_Form.save(commit=False)
			profile.user=user
			profile.save()
			#return redirect('/') 
	else:
		User_Form= RegistroForm()
		Info_Form=infoForm()
	return render(request, 'Registro2.html', {'user_form':User_Form, 'profile_form':Info_Form})	
	#success_url= reverse_lazy ("Home Page")
			#logear usuario
			#return redirect
