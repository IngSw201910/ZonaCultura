from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from homePage.forms import infoForm
from homePage.forms import infoLibro
from homePage.forms import contenidoTarjetaForm
from homePage.forms import contenidoCreditForm
from homePage.models import Carrito
from homePage.models import infousuario
from homePage.models import infoTarjeta
from homePage.forms import RegistroForm
from homePage.forms import logInForm
from homePage.forms import contenidoLiterarioForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import Http404
from homePage.models import ArticulosComprados
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
			return redirect('/HomePage')#TODO: return pagina de inicio despues de iniciar sesion
		else:
			return HttpResponse("Usuario o contraseña no coincide/existe")
	else:
		form=logInForm()
	return render(request, 'paginaInicio.html',{'form':form})
# Create your views here.



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
	return render(request, 'Registro.html', {'user_form':User_Form, 'profile_form':Info_Form})	
	#success_url= reverse_lazy ("Home Page")
			#logear usuario
			#return redirect

@login_required(login_url='/')
def homePage_view(request):
	return render(request, 'HomePage.html')

@login_required(login_url='/')
def subirObra_view (request):
	return render(request,'SubirObra.html');

@login_required(login_url='/')
def subirObraLiteraria_view(request):
	if request.method =='POST':
		Form=contenidoLiterarioForm(request.POST, request.FILES)
		if Form.is_valid():
			producto=Form.save(commit=False)
			producto.user= request.user
			producto.save()
			print("\n***********Formulario valido")
			print("Obra",producto.Titulo," subida, y le quedo una llave primaria de:", producto.id)
			
			return HttpResponse("Submited")
		else:
			print("\n***********Formulario no valido")
			return HttpResponse("Fallo")
	else:
		Form=contenidoLiterarioForm()
	return render(request,'SubirContenidoLiterario.html',{'Form':Form})

@login_required(login_url='/')
def mostrarObraLiteraria(request,primaryKey):
	#allObjects=infoLibro.objects.all()
	#print([p.pk for p in allObjects])
	print(primaryKey)
	try: 
	
		Libro=infoLibro.objects.get(pk=primaryKey)
		if request.GET.get('carrito'):
			print('Hello! el libro con id: ',Libro.id)
			carro=Carrito.objects.create(libro= Libro, usuario=infousuario.objects.get(user=request.user))

			#carro.usuario=infousuario.objects.get(user=request.user)
			
			#print("Usuario:",infousuario.objects.get(user=request.user).id)
	except:
		raise Http404



	return render(request, 'mostrarContentidoLiterario.html' ,{'Libro':Libro})

@login_required(login_url='/')
def comprarCredito_view(request):
	if request.method =='POST':
		Card_Form= contenidoTarjetaForm(request.POST)
		Credit_Form= contenidoCreditForm(request.POST)
		if Card_Form.is_valid() and Credit_Form.is_valid():
			data= Card_Form.cleaned_data
			data2=Credit_Form.cleaned_data
			numeroTarjeta=data.get("numeroTarjeta")
			nombreTitular= data.get("nombreTitular")
			apellidoTitular= data.get("apellidoTitular")
			fechaExpiración= data.get("fechaExpiración")
			codigoSeguridad= data.get("codigoSeguridad")
			balance=data2.get("balance")
			user = infousuario.objects.get(user = request.user)
			user.balance= user.balance+balance
			user.save()
			print("Usuario:",infousuario.objects.get(user=request.user).id)
			print("Usuario:",infousuario.objects.get(user=request.user).balance)
			
			print("\n***********Formulario valido")
			return HttpResponse("Comprado")
			#return redirect('/') 
	else:
		Card_Form =contenidoTarjetaForm()
		Credit_Form =contenidoCreditForm()
		
	return render(request,'CompraCredito.html',{'card_Form':Card_Form,'credit_Form':Credit_Form})

@login_required(login_url='/')
def carrito_view(request):
	usuario= infousuario.objects.get(user = request.user)
	libros=[]
	carri=Carrito.objects.filter(usuario= infousuario.objects.get(user = request.user))
	for item in carri:
		if( item.libro is not None):#Si es un libro
			libros.append(item.libro)


	total=0
	#Sacar total libros

	for p in libros:
		total=total+p.PrecioLibro
	print(usuario.balance)
	if request.GET.get('carrito'):#realizar transacciones
			#print('Hello! el libro con id: ',Libro.id)
			if usuario.balance >= total:# realizar transaccion
				usuario.balance=usuario.balance-total
				print(usuario.balance)
				usuario.save()
				for q in libros:
					p=infousuario.objects.get(user = q.user)
					p.balance=p.balance+q.PrecioLibro
					p.save() 


				for item in carri:
					ArticulosComprados.objects.create(libro= item.libro, usuario=usuario)#esto va a cambiar cuando agregemos multimedia y manualidades
					item.delete() 
				return redirect('/CarritoVista')
			else:
				return redirect('/ComprarCredito')#pagina para comprar credito
	#print("Total ",total )
	#print([p.Titulo for p in libros])
	return render(request,'CarritoVista.html',{'libros':libros, 'Subtotal': total}) 
@login_required(login_url='/')
def comprados_view(request):
	usuario= infousuario.objects.get(user = request.user)
	libros=[]
	comprados =ArticulosComprados.objects.filter(usuario= infousuario.objects.get(user = request.user))
	for item in comprados:
		if( item.libro is not None):#Si es un libro
			libros.append(item.libro)

	return render(request,'VistaComprados.html',{'libros':libros}) 