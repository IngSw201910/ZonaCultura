from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from datetime import date
from homePage.forms import infoForm
from homePage.forms import infoLibro
from homePage.forms import contenidoTarjetaForm
from homePage.forms import contenidoCreditForm
from homePage.models import Carrito
from homePage.models import Comentario
from homePage.models import Donacion
from homePage.models import Compradores
from homePage.models import infousuario
from homePage.models import infoTarjeta
from homePage.models import GeneroLiterario
from homePage.models import GeneroManualidad
from homePage.models import ArticulosComprados
from homePage.models import contenidoMultimedia
from homePage.models import  cuentaPorCobrar
from homePage.models import  BusquedaString
from homePage.forms import comenycaliForm
from homePage.forms import RegistroForm
from homePage.forms import logInForm
from homePage.forms import contenidoLiterarioForm
from homePage.forms import contenidoMultimediaForm
from homePage.forms import DonacionForm
from homePage.forms import contenidoManualidad
from homePage.forms import contenidoManualForm
from homePage.forms import  competenciasForm
from homePage.forms import  generoLiterarioForm
from homePage.forms import  GeneroManualidadForm
from homePage.forms import  BusquedaStringForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import Http404
from django.conf import settings
import os

#from django.core.urlresolvers import reverse_lazy
def index(request):
	print(request.user.pk)
	if(request.user.pk is not None):
		return redirect('/HomePage')
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
		Competencias_Form=competenciasForm(request.POST)
		User_Form= RegistroForm(request.POST)
		Info_Form=infoForm(request.POST,request.FILES)
		if User_Form.is_valid() and Info_Form.is_valid():
			user=User_Form.save()
			competencias=Competencias_Form.save()
			profile=Info_Form.save(commit=False)
			profile.aficiones=competencias
			profile.user=user
			profile.save()
			return redirect('/')
	else:
		Competencias_Form=competenciasForm()
		User_Form= RegistroForm()
		Info_Form=infoForm()
	return render(request, 'Registro.html', {'competencias_Form':Competencias_Form,'user_form':User_Form, 'profile_form':Info_Form})
	#success_url= reverse_lazy ("Home Page")
			#logear usuario
			#return redirect

@login_required(login_url='/')
def homePage_view(request):
	if request.GET.get('Salir'):
		logout(request)
		return redirect('/')
	return render(request, 'HomePage.html')

@login_required(login_url='/')
def perfil_view(request):
	user=infousuario.objects.get(user=request.user)
	if request.GET.get('Salir'):
		logout(request)
		return redirect('/')
	return render(request, 'PerfilPropio.html',{'user':user})

@login_required(login_url='/')
def libros_view(request):
	libros=infoLibro.objects.all()
	contexto={'libros':libros}
	return render(request, 'catalogolibros.html',contexto)

@login_required(login_url='/')
def multimedia_view(request):
	videos=contenidoMultimedia.objects.all()
	contexto={'videos':videos}
	return render(request,'catalogoVideos.html',contexto)

@login_required(login_url='/')
def subirObra_view (request):
	return render(request,'SubirObra.html');

@login_required(login_url='/')
def subirObraLiteraria_view(request):
	if request.method =='POST':
		Form=contenidoLiterarioForm(request.POST, request.FILES)
		Form2=generoLiterarioForm(request.POST)
		if Form.is_valid():
			generos=Form2.save()
			producto=Form.save(commit=False)
			producto.user= request.user
			producto.genero=generos
			producto.save()
			print("\n***********Formulario valido")
			print("Obra",producto.Titulo," subida, y le quedo una llave primaria de:", producto.id)

			return HttpResponse("Submited")
		else:
			print("\n***********Formulario no valido")
			return HttpResponse("Fallo")
	else:
		Form2=generoLiterarioForm()
		Form=contenidoLiterarioForm()
	return render(request,'SubirContenidoLiterario.html',{'Form':Form,'Form2':Form2})
@login_required(login_url='/')
def mostrarObraLiteraria(request,primaryKey):
	#allObjects=infoLibro.objects.all()
	#print([p.pk for p in allObjects])
	print(primaryKey)


	try:

		Libro=infoLibro.objects.get(pk=primaryKey)



		if(ArticulosComprados.objects.filter(usuario=infousuario.objects.get(user = request.user),libro=Libro).first() is not None):
			permitir=False
			print('lo tiene')
		else:
			permitir=True
			print('no lo tiene')
		if request.GET.get('descarga'):
			print (Libro.archivo)
			file_path = os.path.join(settings.MEDIA_ROOT, Libro.archivo.path)
			print(file_path)
			if os.path.exists(file_path):
				with open(file_path, 'rb') as fh:
					response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
					response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
					return response
				#print(file_path)

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
	listaDeGeneros= Libro.genero
	print(listaDeGeneros)
	aux=''
	if listaDeGeneros.Comedia==True :
		print('Es de Comedia')
		aux=aux+'Comedia '
	if listaDeGeneros.Drama==True :
		aux=aux+'Drama '
	if listaDeGeneros.Tragicomedia==True :
		aux=aux+'Tragicomedia '
	if listaDeGeneros.Terror==True :
		aux=aux+'Terror '
	if listaDeGeneros.Ciencia_Ficción==True :
		aux=aux+'Ciencia Ficción '
	if permitir:
		return render(request, 'mostrarContentidoLiterario.html',{'Libro':Libro,'generos':aux})
	else:
		return render(request, 'mostrarContentidoLiterarioSiYaLoTieneComprado.html',{'Libro':Libro,'generos':aux})

@login_required(login_url='/')
def mostrarMultimedia(request,primaryKey):
	video=contenidoMultimedia.objects.get(pk=primaryKey)
	return render(request,'mostrarContenidoMultimedia.html',{'video':video})

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
			mesExpiracion= data.get("mesExpiracion")
			anoExpiracion= data.get("anoExpiracion")
			codigoSeguridad= data.get("codigoSeguridad")
			existe=0
			for numTarj in infoTarjeta.objects.all():
				if numeroTarjeta== numTarj.numeroTarjeta :
					if nombreTitular== numTarj.nombreTitular:
						if apellidoTitular==numTarj.apellidoTitular:
							if mesExpiracion==numTarj.mesExpiracion:
								if anoExpiracion==numTarj.anoExpiracion:
									if codigoSeguridad==numTarj.codigoSeguridad:
										anoExpiracion=anoExpiracion+2000
										if(anoExpiracion==date.today().year):
											if(mesExpiracion<date.today().month):
												print("ano",date.today().year)
												print("vergas")
												return HttpResponse("La tarjeta es valida pero ya esta vencida")
											else:
												existe=existe+1
										else:
											existe=existe+1


			if existe==1:

				balance=data2.get("balance")
				user = infousuario.objects.get(user = request.user)
				user.balance= user.balance+balance
				user.save()
				print("Usuario:",infousuario.objects.get(user=request.user).id)
				print("Usuario:",infousuario.objects.get(user=request.user).balance)

				print("\n***********Formulario valido")
				return HttpResponse("Comprado")
			else:
				return HttpResponse("La tarjeta no existe o ingreso algún campo erroneo")

			#return redirect('/')
	else:
		Card_Form =contenidoTarjetaForm()
		Credit_Form =contenidoCreditForm()

	return render(request,'CompraCredito.html',{'card_Form':Card_Form,'credit_Form':Credit_Form})

@login_required(login_url='/')
def carrito_view(request):
	if request.GET.get('Salir'):
		logout(request)
		return redirect('/')
	usuario= infousuario.objects.get(user = request.user)
	libros=[]
	manualidades=[]
	carri=Carrito.objects.filter(usuario= infousuario.objects.get(user = request.user))
	cantidad=0
	for item in carri:
		if( item.libro is not None):#Si es un libro
			libros.append(item.libro)
			cantidad=cantidad+1
		if( item.manualidad is not None):
			manualidades.append(item.manualidad)
			cantidad=cantidad+1


	total=0

	#Sacar total libros

	for p in libros:
		total=total+p.PrecioLibro

	for m in manualidades:
		if(m.existencias!=0):
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



				for item in carri:
					if(item.libro is not None):
						ArticulosComprados.objects.create(libro= item.libro, usuario=usuario)#esto va a cambiar cuando agregemos multimedia y manualidades
						usuarioD= infousuario.objects.get(user =item.libro.user)
						Compradores.objects.create(libro=item.libro,usuarioDuenio=usuarioD,usuarioComprador=usuario)
						item.delete()
						cantidad=cantidad-1
					if(item.manualidad is not None and item.manualidad.existencias !=0):
						ArticulosComprados.objects.create(manualidad= item.manualidad, usuario=usuario)#esto va a cambiar cuando agregemos multimedia y manualidades
						usuarioDd= infousuario.objects.get(user =item.manualidad.user)
						item.manualidad.existencias=item.manualidad.existencias-1
						item.manualidad.save()
						Compradores.objects.create(manualidad=item.manualidad,usuarioDuenio=usuarioDd,usuarioComprador=usuario)
						item.delete()
						cantidad=cantidad-1
				print("hola cssantidad")
				print(cantidad)
				if(cantidad!=0):
					print("hola cantidad")
					print(cantidad)
					return HttpResponse("No se pudieron comprar todos los elemntos, verifique quizás las existencias del articulo se agotaron ")
				else:
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
			if Usuario.es_CreadorDeContenido :
				data= Donacion_Form.cleaned_data
				cantida=data.get("cantidad")
				msj=data.get("mensaje")
				print(cantida)
				

				#print(Usu)
				if Usua.balance>=cantida:
					Doni=Donacion.objects.create( usuarioDonante=Usua,usuarioBen=Usuario,cantidad=cantida,mensaje=msj)
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
				return HttpResponse("El usuario al que desea donar no es creador de contenido, si desea donar por favor busque un creador de contenido")




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
		Form2=GeneroManualidadForm(request.POST)
		
		if Form.is_valid():

			generos=Form2.save()

			

			producto=Form.save(commit=False)
			producto.user= request.user
			producto.genero=generos

			

			producto.save()
			print("\n***********Formulario valido")
			print("Obra",producto.title," subida, y le quedo una llave primaria de:", producto.id)

			return HttpResponse("Submited")
		else:
			print("\n***********Formulario no valido")
			return HttpResponse("Fallo")
	else:
		
		Form2=GeneroManualidadForm()
		Form=contenidoManualForm()
	return render(request,'SubirManualidad.html',{'Form':Form,'Form2':Form2})

@login_required(login_url='/')
def mostrarManualidad(request,primaryKey):
	#allObjects=infoLibro.objects.all()
	#print([p.pk for p in allObjects])
	print(primaryKey)
	try:

		usuario= infousuario.objects.get(user = request.user)
		Manualidad=contenidoManualidad.objects.get(pk=primaryKey)
		comenn=Comentario.objects.filter(manu=Manualidad)
		com=[]
		for cc in comenn:
			if(cc is not None):
				com.append(cc)


		print(usuario.user.username)

		if request.GET.get('carrito'):
			#c=Carrito.objects.filter(manualidad=Manualidad,usuario=infousuario.objects.get(user=request.user)).first()
			#print(c)

			if(Manualidad.existencias!=0):
				carro=Carrito.objects.create(manualidad= Manualidad, usuario=infousuario.objects.get(user=request.user))
				print(carro.manualidad.title)
				return redirect('/CarritoVista')
			else :
				return HttpResponse("No se pudo añadir")

	except:
		raise Http404

	listaDeGeneros=Manualidad.genero
	print(listaDeGeneros)
	aux=''
	if listaDeGeneros.Bodegon==True :
		print('Es Bodegon')
		aux=aux+'Bodegón '
	if listaDeGeneros.Vanitas==True :
		aux=aux+'Vanitas '
	if listaDeGeneros.Retrato==True :
		aux=aux+'Retrato '
	if listaDeGeneros.Terror==True :
		aux=aux+'Terror '
	if listaDeGeneros.Desnudo==True :
		aux=aux+'Desnudo '
	if listaDeGeneros.Religioso==True :
		aux=aux+'Religioso '
	if listaDeGeneros.Historico==True :
		aux=aux+'Histórico '
	if listaDeGeneros.Mitologico==True :
		aux=aux+'Mitológico '
	if listaDeGeneros.Paisaje==True :
		aux=aux+'Paisaje '
	if listaDeGeneros.Funeraria==True :
		aux=aux+'Funeraria '
	if listaDeGeneros.Monumento==True :
		aux=aux+'Monumento '
	if listaDeGeneros.Estatuilla==True :
		aux=aux+'Estatuilla '
	if listaDeGeneros.Figura==True :
		aux=aux+'Figura '
	if listaDeGeneros.Relieve==True :
		aux=aux+'Relieve '

	return render(request, 'mostrarManualidad.html' ,{'Manualidad':Manualidad,'com':com,'usuario':usuario,'generos':aux})

@login_required(login_url='/')
def editarManualidades_view(request,primaryKey):
	Manualidad=contenidoManualidad.objects.get(pk=primaryKey)
	print("aca llegue2")
	if Manualidad.user.pk != request.user.pk: ##LO AGREGO SANTIAGO
		raise Http404							##PORQUE RECUERDEN QUE SI EL AUTOR NO SOY YO NO PUEDO EDITAR
	if request.method =='POST':
		print("entre")
		print("aca llegue1")
		Form=contenidoManualForm(request.POST, request.FILES,instance=Manualidad)
		Form2=GeneroManualidadForm(request.POST,instance=Manualidad.genero)
		print("aca llegue")
		if Form.is_valid():
			generos=Form2.save()
			producto=Form.save(commit=False)
			producto.user= request.user
			producto.genero=generos
			producto.save()
			print("\n***********Formulario valido")
			print("Obra",producto.title," subida, y le quedo una llave primaria de:", producto.id)

			return HttpResponse("Submited")
		else:
			Form = EmpleadoForm(instance=Manualidad)
			print("\n***********Formulario no valido")
			return HttpResponse("Fallo")
	else:
		Form2=GeneroManualidadForm(instance=Manualidad.genero)
		Form=contenidoManualForm(instance=Manualidad)

	return render(request,'EditarManualidad.html',{'Form':Form,'Form2':Form2})
@login_required(login_url='/')
def comentarios_calificacionManu(request,primaryKey):
	Manualidad=contenidoManualidad.objects.get(pk=primaryKey)
	usu = infousuario.objects.get(user = request.user)

	if request.method =='POST':
		if(Manualidad.user.username==usu.user.username):
			return HttpResponse("No puede comentar su propia obra")
		else:
			com= comenycaliForm(request.POST)
			if com.is_valid():
				data= com.cleaned_data
				calif=data.get("califi")

				suma=Manualidad.puntaje*Manualidad.canticomp
				suma=suma+calif
				print("sum")
				print(suma)
				Manualidad.canticomp=Manualidad.canticomp+1
				Manualidad.puntaje=suma/Manualidad.canticomp
				print("cc")
				print(Manualidad.canticomp)

				Manualidad.save()
				comentar= data.get("comentario")
				cc=Comentario.objects.create(manu=Manualidad,califi=calif,comentario=comentar,usuarioComentador=usu)
				print("\n***********Formulario valido")
				return HttpResponse("Comentario enviado")
			#return redirect('/')
	else:
		com =comenycaliForm()

	return render(request,'comentarManu.html',{'com':com,'Manualidad':Manualidad})

@login_required(login_url='/')
def editarContenidoLiterario_view(request,primaryKey):
	Libro=infoLibro.objects.get(pk=primaryKey)
	if Libro.user.pk != request.user.pk:
		raise Http404
	else:
		if request.method =='POST':
			Form=contenidoLiterarioForm(request.POST, request.FILES,instance=Libro)
			Form2=generoLiterarioForm(request.POST,instance=Libro.genero)
			print("aca llegue")
			if Form.is_valid():
				generos=Form2.save()
				producto=Form.save(commit=False)
				producto.user= request.user
				producto.genero=generos
				producto.save()

				print("Obra",producto.Titulo," subida, y le quedo una llave primaria de:", producto.pk)

				return HttpResponse("Submited")
			else:
				print("\n***********Formulario no valido")
				return HttpResponse("Fallo")
		else:
			Form=contenidoLiterarioForm(instance=Libro)
			Form2=generoLiterarioForm(instance=Libro.genero)

		return render(request,'EditarManualidad.html',{'Form':Form,'Form2':Form2})

@login_required(login_url='/')
def editarUsuarioInfo(request):
	#asegurarse que el usuario sea el mismo
	usuario=infousuario.objects.get(user=request.user)
	if request.method =='POST':
		Form=RegistroForm(request.POST,instance=usuario.user)
		Form2=competenciasForm(request.POST,instance=usuario.aficiones)
		Form3=infoForm(request.POST,request.FILES,instance=usuario)
		print("aca llegue")
		if Form.is_valid():
			user=Form.save()
			competencias=Form2.save()
			profile=Form3.save(commit=False)
			profile.aficiones=competencias
			profile.user=user
			profile.save()
			return HttpResponse("Submited")
		else:
			print("\n***********Formulario no valido")
			return HttpResponse("Fallo")
	else:
		Form=RegistroForm(instance=usuario.user)
		Form2=competenciasForm(instance=usuario.aficiones)
		Form3=infoForm(instance=usuario)
	return render(request,'Registro2.html',{'user_form':Form,'competencias_Form':Form2,'profile_form':Form3})


@login_required(login_url='/')
def busquedaObraGeneral_view(request):

	libros = infoLibro.objects.all()
	manualidades = contenidoManualidad.objects.all()

	librosPasan=[]
	manualidadesPasan=[]

	for libro in libros:
		if "q" in libro.Titulo:
				librosPasan.append(libro)

	for manualidad in manualidades:
		if "q" in manualidad.title:
				manualidadesPasan.append(manualidad)

	context = {
		'librosPasan':librosPasan,
		'manualidadesPasan':manualidadesPasan
	}

	return render(request,'BusquedaGeneral.html',context)

@login_required(login_url='/')
def busquedaObraEspecifica_view(request):

	return render(request,'BusquedaEspecifica.html')

@login_required(login_url='/')
def busquedaObraLiteraria_view(request):

	return render(request, 'BusquedaObraLiteraria.html')

@login_required(login_url='/')
def busquedaObraManualidad_view(request):

	return render(request, 'BusquedaObraManualidad.html')
@login_required(login_url='/')
def BuscarString(request):
	#asegurarse que el usuario sea el mismo
	manualidadex=[]
	usuario=infousuario.objects.get(user=request.user)
	if request.method =='POST':
		Form=BusquedaStringForm(request.POST)
		if Form.is_valid():
			busqueda=Form.save()
			busqueda.generoBusqueda=busqueda.generoBusqueda


			Mani=contenidoManualidad.objects.all()
			for m in Mani:
				print("aca")
				print(m.genero)
				if m.genero==busqueda.generoBusqueda:

					manualidadex.append(m)
					print ("hola"+manualidadex.genero)
		else:
			
			return HttpResponse("Fallo")
	else:
		Form=BusquedaStringForm()
	return render(request,'vistaBusquedaS.html',{'Form':Form,'manualidadex':manualidadex})
