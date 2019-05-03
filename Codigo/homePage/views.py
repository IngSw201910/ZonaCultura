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
from homePage.models import Donacion
from homePage.models import Compradores
from homePage.models import infousuario
from homePage.models import infoTarjeta
from homePage.models import contenidoMultimedia
from homePage.forms import RegistroForm
from homePage.forms import logInForm
from homePage.forms import contenidoLiterarioForm
from homePage.forms import contenidoMultimediaForm
from homePage.forms import DonacionForm
from homePage.forms import contenidoManualidad
from homePage.forms import contenidoManualForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
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
		Info_Form=infoForm(request.POST,request.FILES)
		if User_Form.is_valid() and Info_Form.is_valid():
			user=User_Form.save()
			profile=Info_Form.save(commit=False)
			profile.user=user
			profile.save()
			return redirect('/') 
	else:
		User_Form= RegistroForm()
		Info_Form=infoForm()
	return render(request, 'Registro.html', {'user_form':User_Form, 'profile_form':Info_Form})	
	#success_url= reverse_lazy ("Home Page")
			#logear usuario
			#return redirect

@login_required(login_url='/')
def homePage_view(request):
	if request.GET.get('Salir'):
		print("hola")
		return redirect('/')
	return render(request, 'HomePage.html')

@login_required(login_url='/')
def perfil_view(request):
	user=infousuario.objects.get(user=request.user)
	return render(request, 'Perfil.html',{'user':user})	

@login_required(login_url='/')
def libros_view(request):
	libros=infoLibro.objects.all()
	contexto={'libros':libros}
	return render(request, 'catalogolibros.html',contexto)

@login_required(login_url='/')
def multimedia_view(request):
	videos=contenidoMultimedia.objects.all()
	contexto={'videos':videos}
	return render(request,'catalogoMultimedia.html',contexto)

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
			c=Carrito.objects.filter(libro=Libro,usuario=infousuario.objects.get(user=request.user)).first()
			print(c)
			if c is None :
				carro=Carrito.objects.create(libro= Libro, usuario=infousuario.objects.get(user=request.user))
				return redirect('/CarritoVista')
			else:
				return HttpResponse("Usted ya tiene este elemento en el carrito")

			#carro.usuario=infousuario.objects.get(user=request.user)
			
			#print("Usuario:",infousuario.objects.get(user=request.user).id)
	except:
		raise Http404
	return render(request, 'mostrarContentidoLiterario.html' ,{'Libro':Libro})
@login_required(login_url='/')
def mostrarMultimedia(request,primaryKey):
	video=contenidoMultimedia.objects.get(pk=primaryKey)
	return render(request,'mostrarContentidoMultimedia.html',{'video':video})

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
	manualidades=[]
	carri=Carrito.objects.filter(usuario= infousuario.objects.get(user = request.user))
	for item in carri:
		if( item.libro is not None):#Si es un libro
			libros.append(item.libro)
		if( item.manualidad is not None and item.manualidad.existencias!=0):
			manualidades.append(item.manualidad)


	total=0
	#Sacar total libros

	for p in libros:
		total=total+p.PrecioLibro
	for m in manualidades:
		total=total+m.precioV
		#print(usuario.balance)
	#if request.GET.get('name'):
	#		produc=infoLibro.objects.get(Titulo=request.libro.Titulo)
			#print(produc.Titulo)
			#print(produc)
    	 	#carri.remove(produc)

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
				for n in manualidades:
					if(n.existencias!=0):
						m=infousuario.objects.get(user=n.user)
						m.balance=m.balance+n.precioV
						n.existencias=n.existencias-1

				for item in carri:
					if(item.libro is not None):
						ArticulosComprados.objects.create(libro= item.libro, usuario=usuario)#esto va a cambiar cuando agregemos multimedia y manualidades
						usuarioD= infousuario.objects.get(user =item.libro.user)
						Compradores.objects.create(libro=item.libro,usuarioDuenio=usuarioD,usuarioComprador=usuario)
					if(item.manualidad is not None):
						ArticulosComprados.objects.create(manualidad= item.manualidad, usuario=usuario)#esto va a cambiar cuando agregemos multimedia y manualidades
						usuarioDd= infousuario.objects.get(user =item.manualidad.user)
						Compradores.objects.create(manualidad=item.manualidad,usuarioDuenio=usuarioDd,usuarioComprador=usuario)
					item.delete() 
				return redirect('/CarritoVista')
			else:
				return redirect('/CompraCredito')#pagina para comprar credito
	elif request.GET.get('borrar'):
		for item in carri:
			item.delete()
		return redirect('/CarritoVista')
	else:
		for libro in libros:
			aux="Libro"+str(libro.pk)
			aux=aux.strip()
			print(aux)
			if request.GET.get(aux) is not None:
				print('Encontro articulo')
				carr=Carrito.objects.filter(libro=libro,usuario=usuario)
				carr[0].delete()
				return redirect('/CarritoVista')
		for manual in manualidades:
			aux1="Manual"+str(manual.pk)
			aux1=aux1.strip()
			print(aux1)
			if request.GET.get(aux1) is not None:
				print('Encontro articulo')
				carr=Carrito.objects.filter(manualidad=manual,usuario=usuario)
				carr[0].delete()
				return redirect('/CarritoVista')
	#print("Total ",total )
	#print([p.Titulo for p in libros])
	return render(request,'CarritoVista.html',{'libros':libros, 'manualidades': manualidades,'Subtotal': total,'carrito':carri}) 
@login_required(login_url='/')
def comprados_view(request):
	usuario= infousuario.objects.get(user = request.user)
	libros=[]
	manualidades=[]
	comprados =ArticulosComprados.objects.filter(usuario= infousuario.objects.get(user = request.user))
	for item in comprados:
		if( item.libro is not None):#Si es un libro
			libros.append(item.libro)
		if( item.manualidad is not None):#Si es un libro
			manualidades.append(item.manualidad)

	return render(request,'VistaComprados.html',{'libros':libros,'manualidades':manualidades}) 
@login_required(login_url='/')
def compradores_view(request):
	usuario= infousuario.objects.get(user = request.user)
	usuariosCompradores=[]
	usuariosCompraManu=[]
	compradxres=Compradores.objects.filter(usuarioDuenio=infousuario.objects.get(user = request.user))
	for item in compradxres:
		if( item.usuarioComprador is not None and item.libro is not None ):#Si es un libro
			usuariosCompradores.append(item)
		if( item.usuarioComprador is not None and item.manualidad is not None ):#Si es un libro
			usuariosCompraManu.append(item)

	return render(request,'VistaCompradores.html',{'usuariosCompradores':usuariosCompradores,'usuariosCompraManu':usuariosCompraManu}) 
def SubirContenidoMultimedia_view(request):
    if request.method=='POST':
        multimedia_form=contenidoMultimediaForm(request.POST)
        if multimedia_form.is_valid():
            return HttpResponse("Submited")
        else:
            return HttpResponse("Fallo")
    else:
        multimedia_form=contenidoMultimediaForm()
    return render(request,'SubirVideo.html',{'multimedia_form': multimedia_form})

@login_required(login_url='/')
def Donacion_view(request,primaryKey):
	if request.method =='POST':
		Donacion_Form =DonacionForm(request.POST)
		if Donacion_Form.is_valid():
			Usuario=infousuario.objects.get(pk=primaryKey)
			Usua=infousuario.objects.get(user=request.user)
			data= Donacion_Form.cleaned_data
			cantida=data.get("cantidad")
			print(cantida)

			#print(Usu)
			if Usua.balance>=cantida:
				Doni=Donacion.objects.create( usuarioDonante=Usua,usuarioBen=Usuario,cantidad=cantida)
				usu=infousuario.objects.get(user=request.user)
				usu.balance=usu.balance - cantida
				usu.save()
				Usuario.balance=Usuario.balance+cantida
				Usuario.save()
				print("donit")
				print(Usuario.balance)
				return HttpResponse("Donacion satisfactoria")
			else:
				return redirect('/CompraCredito')


			
	else:
		Donacion_Form=DonacionForm()
		
	return render(request,'VistaDonacion.html',{'UsuariBeni':infousuario.objects.get(pk=primaryKey),'Donacion_Form':Donacion_Form})
@login_required(login_url='/')
def mostrarUsuario(request,primaryKey):
	try: 	
		Usu=infousuario.objects.get(pk=primaryKey)
		print("hola1")
	except:
		raise Http404
	return render(request, 'VistaUsuario.html' ,{'Usu':Usu})
@login_required(login_url='/')
def donadores_view(request):
	usuario= infousuario.objects.get(user = request.user)
	usuariosDonadores=[]
	donadorex=Donacion.objects.filter(usuarioBen=infousuario.objects.get(user = request.user))
	for item in donadorex:
		if( item.usuarioDonante is not None and item.cantidad is not None ):#Si es un libro
			usuariosDonadores.append(item)

	return render(request,'VistaDonantes.html',{'usuariosDonadores':usuariosDonadores}) 
@login_required(login_url='/')
def AquienDone_view(request):
	usuario= infousuario.objects.get(user = request.user)
	usuariosQDone=[]
	donadorex=Donacion.objects.filter(usuarioDonante=infousuario.objects.get(user = request.user))
	for item in donadorex:
		if( item.usuarioBen is not None and item.cantidad is not None ):#Si es un libro
			usuariosQDone.append(item)

	return render(request,'AquienDone.html',{'usuariosQDone':usuariosQDone}) 

@login_required(login_url='/')
def subirManualidades_view(request):
	if request.method =='POST':
		Form=contenidoManualForm(request.POST, request.FILES)
		if Form.is_valid():
			producto=Form.save(commit=False)
			producto.user= request.user
			producto.save()
			print("\n***********Formulario valido")
			print("Obra",producto.title," subida, y le quedo una llave primaria de:", producto.id)
			
			return HttpResponse("Submited")
		else:
			print("\n***********Formulario no valido")
			return HttpResponse("Fallo")
	else:
		Form=contenidoManualForm()
	return render(request,'SubirManualidad.html',{'Form':Form})
@login_required(login_url='/')
def mostrarManualidad(request,primaryKey):
	#allObjects=infoLibro.objects.all()
	#print([p.pk for p in allObjects])
	print(primaryKey)
	try:
		print("hola")
		Manualidad=contenidoManualidad.objects.get(pk=primaryKey)
		if request.GET.get('carrito'):
			#c=Carrito.objects.filter(manualidad=Manualidad,usuario=infousuario.objects.get(user=request.user)).first()
			#print(c)
			if(Manualidad.existencias!=0):
				carro=Carrito.objects.create(manualidad= Manualidad, usuario=infousuario.objects.get(user=request.user))
				print(carro.manualidad.title)
				return redirect('/CarritoVista')
			else :
				return HttpResponse("No hay unidades")

			

	except:
		raise Http404
	return render(request, 'mostrarManualidad.html' ,{'Manualidad':Manualidad})

@login_required(login_url='/')
def editarManualidades_view(request,primaryKey):
	 
	Manualidad=contenidoManualidad.objects.get(pk=primaryKey)
	print("aca llegue2")
	if request.method =='POST':
		print("entre")
		print("aca llegue1")
		Form=contenidoManualForm(request.POST, request.FILES,instance=Manualidad)
		print("aca llegue")
		if Form.is_valid():
			producto=Form.save(commit=False)
			producto.user= request.user
			producto.save()
			print("\n***********Formulario valido")
			print("Obra",producto.title," subida, y le quedo una llave primaria de:", producto.id)
				
			return HttpResponse("Submited")
		else:
			Form = EmpleadoForm(instance=Manualidad)
			print("\n***********Formulario no valido")
			return HttpResponse("Fallo")
	else:
		Form=contenidoManualForm(instance=Manualidad)
		print("que pasa mani")
	
	return render(request,'EditarManualidad.html',{'Form':Form})
