from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from homePage.models import *
from homePage.forms import *
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import Http404
from django.conf import settings
from collections import Counter
from datetime import datetime
import os



def establecerContacto(usuario1, usuario2):
	Contactos.objects.create(Pasivo=usuario2, Activo=usuario1)
	Contactos.objects.create(Activo=usuario2, Pasivo=usuario1)
@login_required(login_url='/')
def vistaContactos(request):
	infoContactos=[]
	hayContactos=True;
	listaContactos=Contactos.objects.filter(Activo=request.user)
	for q in listaContactos:
		p=infousuario.objects.get(user = q.Pasivo)
		infoContactos.append(p)
	if len(listaContactos) ==0 :
		print("no hay Contactos")
		hayContactos=False
	for contactos in infoContactos:
			aux1=""+str(contactos.user.pk)
			aux1=aux1.strip()
			#print(aux1)
			if request.GET.get(aux1) is not None:
				print('Encontro articulo')
				url= '/EnviarMensaje/'+aux1
				print(url)
				return redirect(url)
	return render(request,'verContactos.html',{'infoContactos':infoContactos,'hayContactos':hayContactos})

@login_required(login_url='/')
def EnviarMensaje(request, primaryKey):
	esContato=False
	listaContactos=Contactos.objects.filter(Activo=request.user)
	for q in listaContactos:
		if q.Pasivo.pk == primaryKey:
			esContato=True
	if esContato ==False:
		raise Http404
	if request.method =='POST':
		form=MensajeForm(request.POST or None)
		if form.is_valid():
			mensaje=form.save(commit=False)
			mensaje.Emisor=request.user
			mensaje.Receptor=User.objects.get(id=primaryKey)
			mensaje.fecha=datetime.now()
			mensaje.save()
			return HttpResponse("Mensaje Enviado")
		#end if
	else:
		form=MensajeForm()
	#end else
	return render(request,'EnviarMensaje.html',{'Form':form})


@login_required(login_url='/')
def bandejaView (request):
	hayMensajes=True
	listaMensajes=Mensajes.objects.order_by('-fecha').filter(Receptor=request.user)
	for Mensaje in listaMensajes:
			aux1=str(Mensaje.pk)
			aux1=aux1.strip()
			if request.GET.get(aux1) is not None:
				Mensaje.delete()
				return redirect('/BandejaEntrada')
	if len(listaMensajes)==0:
		hayMensajes=False
	return render(request, 'Bandeja.html',{'listaMensajes':listaMensajes, 'hayMensajes':hayMensajes})





@login_required(login_url='/')
def mensajeView(request, primaryKey):
	Mensaje=Mensajes.objects.get(pk=primaryKey, Receptor=request.user)
	if request.GET.get('responder'):
		return redirect('/EnviarMensaje/'+str(Mensaje.Emisor.pk))
	if Mensaje is not None:
		return render(request, 'visualizarMensaje.html',{'Mensaje':Mensaje})
	else:
		raise Http404




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
	if request.GET.get('serColaborador'):
		print('entro')
		user.es_Colaborador= True
		user.save()
		return redirect('/Perfil')
	if request.GET.get('NoserColaborador'):
		user.es_Colaborador= False
		user.save()
		return redirect('/Perfil')



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
	comentarios=ComentarioObraLiteraria.objects.filter(libro=Libro)
	hayComentarios=True
	promedioCalificacion=0
	if len(comentarios)== 0:
		hayComentarios=False
	else:
		for comentario in comentarios:
			promedioCalificacion=promedioCalificacion+comentario.califi
		promedioCalificacion=promedioCalificacion/len(comentarios)
	return render(request, 'mostrarContentidoLiterario.html',{'Libro':Libro,'generos':aux, 'permitir':permitir, 'hayComentarios':hayComentarios, 'comentarios':comentarios, 'promedioCalificacion':promedioCalificacion})


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
		if request.GET.get('contratar'):
			return redirect('/')
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
def comentarios_calificacionLibro(request,primaryKey):
	Libro=infoLibro.objects.get(pk=primaryKey)
	usu = infousuario.objects.get(user = request.user)

	aux=ArticulosComprados.objects.filter(usuario=usu, libro=Libro)
	aux2= ComentarioObraLiteraria.objects.filter(usuarioComentador=usu, libro=Libro)
	if len(aux2)==0:
		if  len(aux) >0:
			if request.method =='POST':
				if(Libro.user.username==usu.user.username):
					return HttpResponse("No puede comentar su propia obra")
				else:
					com= comenycaliFormLibro(request.POST)
					if com.is_valid():
						comentario=com.save(commit=False)
						comentario.libro=Libro
						comentario.usuarioComentador=usu
						comentario.save()
						print("\n***********Formulario valido")
						return HttpResponse("Comentario enviado")
					#return redirect('/')
			else:
				com = comenycaliFormLibro()
		else:
			raise Http404
	else:
		raise Http404
	return render(request,'comentarLibro.html',{'com':com,'Libro':Libro})

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
def busquedaColaboradores_view(request):
	usuario=infousuario.objects.get(user=request.user)
	if request.GET.get('Salir'):
		logout(request)
		return redirect('/')
	return render(request,'BusquedaColaboradores.html')

@login_required(login_url='/')
def busquedaColaboradoresResultado_view(request):
	usuario=infousuario.objects.get(user=request.user)
	if request.GET.get('Salir'):
		logout(request)
		return redirect('/')

	colaboradores = infousuario.objects.all()

	palabra = request.POST.get('buscarstring')
	print(palabra)

	colaboradoresPasan=[]
	pasanCombo = []

	if palabra is "" and not 'check1' in request.POST and not 'check2'in request.POST and not 'check3'in request.POST and not 'check4'in request.POST and not 'check5'in request.POST and not 'check6' in request.POST and not 'check7'in request.POST and not 'check8'in request.POST and not 'check9'in request.POST and not 'check10'in request.POST and not 'check11' in request.POST and not 'check12'in request.POST and not 'check13'in request.POST and not 'check14'in request.POST:
		return HttpResponse("No utilizó ninguna forma de búsqueda. Por favor vuelva a intentarlo.")

	if palabra is "":
		for colaborador in colaboradores:
			if 'check1' in request.POST:
				if colaborador.aficiones.Escritor:
					colaboradoresPasan.append(colaborador)
			if 'check2' in request.POST:
				if colaborador.aficiones.Pintor:
					colaboradoresPasan.append(colaborador)
			if 'check3' in request.POST:
				if colaborador.aficiones.Escultor:
					colaboradoresPasan.append(colaborador)
			if 'check4' in request.POST:
				if colaborador.aficiones.Cantante:
					colaboradoresPasan.append(colaborador)
			if 'check5' in request.POST:
				if colaborador.aficiones.Guitarrista:
					colaboradoresPasan.append(colaborador)
			if 'check6' in request.POST:
				if colaborador.aficiones.Bajista:
					colaboradoresPasan.append(colaborador)
			if 'check7' in request.POST:
				if colaborador.aficiones.Pianista:
					colaboradoresPasan.append(colaborador)
			if 'check8' in request.POST:
				if colaborador.aficiones.Baterista:
					colaboradoresPasan.append(colaborador)
			if 'check9' in request.POST:
				if colaborador.aficiones.Violinista:
					colaboradoresPasan.append(colaborador)
			if 'check10' in request.POST:
				if colaborador.aficiones.Saxofonista:
					colaboradoresPasan.append(colaborador)
			if 'check11' in request.POST:
				if colaborador.aficiones.Acordeonista:
					colaboradoresPasan.append(colaborador)
			if 'check12' in request.POST:
				if colaborador.aficiones.Trompetista:
					colaboradoresPasan.append(colaborador)
			if 'check13' in request.POST:
				if colaborador.aficiones.Fotografo:
					colaboradoresPasan.append(colaborador)
			if 'check14' in request.POST:
				if colaborador.aficiones.Actor:
					colaboradoresPasan.append(colaborador)

		if not colaboradoresPasan:
			context = {
				'colaboradoresPasan': colaboradoresPasan
			}
		else:
			count = Counter(colaboradoresPasan)
			count.most_common(1)[0][0]
			context = {
				'colaboradoresPasan': count
			}

		return render(request, 'BusquedaColaboradoresResultado.html', context)

	for colaborador in colaboradores:
		if palabra in colaborador.user.username:
				colaboradoresPasan.append(colaborador)

	if not 'check1' in request.POST and not 'check2'in request.POST and not 'check3'in request.POST and not 'check4'in request.POST and not 'check5'in request.POST and not 'check6' in request.POST and not 'check7'in request.POST and not 'check8'in request.POST and not 'check9'in request.POST and not 'check10'in request.POST and not 'check11' in request.POST and not 'check12'in request.POST and not 'check13'in request.POST and not 'check14'in request.POST:
		if not colaboradoresPasan:
			context = {
				'colaboradoresPasan': colaboradoresPasan
			}
		else:
			count = Counter(colaboradoresPasan)
			count.most_common(1)[0][0]
			context = {
				'colaboradoresPasan': count
			}

		return render(request, 'BusquedaColaboradoresResultado.html', context)

	for colaborador in colaboradoresPasan:
		if 'check1' in request.POST:
			if colaborador.aficiones.Escritor:
				pasanCombo.append(colaborador)
		if 'check2' in request.POST:
			if colaborador.aficiones.Pintor:
				pasanCombo.append(colaborador)
		if 'check3' in request.POST:
			if colaborador.aficiones.Escultor:
				pasanCombo.append(colaborador)
		if 'check4' in request.POST:
			if colaborador.aficiones.Cantante:
				pasanCombo.append(colaborador)
		if 'check5' in request.POST:
			if colaborador.aficiones.Guitarrista:
				pasanCombo.append(colaborador)
		if 'check6' in request.POST:
			if colaborador.aficiones.Bajista:
				pasanCombo.append(colaborador)
		if 'check7' in request.POST:
			if colaborador.aficiones.Pianista:
				pasanCombo.append(colaborador)
		if 'check8' in request.POST:
			if colaborador.aficiones.Baterista:
				pasanCombo.append(colaborador)
		if 'check9' in request.POST:
			if colaborador.aficiones.Violinista:
				pasanCombo.append(colaborador)
		if 'check10' in request.POST:
			if colaborador.aficiones.Saxofonista:
				pasanCombo.append(colaborador)
		if 'check11' in request.POST:
			if colaborador.aficiones.Acordeonista:
				pasanCombo.append(colaborador)
		if 'check12' in request.POST:
			if colaborador.aficiones.Trompetista:
				pasanCombo.append(colaborador)
		if 'check13' in request.POST:
			if colaborador.aficiones.Fotografo:
				pasanCombo.append(colaborador)
		if 'check14' in request.POST:
			if colaborador.aficiones.Actor:
				pasanCombo.append(colaborador)

	if not pasanCombo:
		context = {
			'colaboradoresPasan': pasanCombo
		}
	else:
		count = Counter(pasanCombo)
		count.most_common(1)[0][0]
		context = {
			'colaboradoresPasan': count
		}

	return render(request, 'BusquedaColaboradoresResultado.html', context)

@login_required(login_url='/')
def busquedaObraGeneral_view(request):
	usuario=infousuario.objects.get(user=request.user)
	if request.GET.get('Salir'):
		logout(request)
		return redirect('/')

	libros = infoLibro.objects.all()
	manualidades = contenidoManualidad.objects.all()
	videos = contenidoMultimedia.objects.all()

	#if request.method =='POST':
		#print('*'*50)
		#print(request.POST)
		#print('*'*50)

	palabra = request.POST.get('buscarstring')
	print(palabra)

	librosPasan=[]
	manualidadesPasan=[]
	videosPasan=[]

	if palabra is None:
		return HttpResponse("Fallo")

	for libro in libros:
		if palabra in libro.Titulo:
				librosPasan.append(libro)

	for manualidad in manualidades:
		if palabra in manualidad.title:
				manualidadesPasan.append(manualidad)

	for video in videos:
		if palabra in video.title:
			videosPasan.append(video)

	context = {
		'librosPasan':librosPasan,
		'manualidadesPasan':manualidadesPasan,
		'videosPasan':videosPasan
	}

	return render(request,'BusquedaGeneral.html',context)

@login_required(login_url='/')
def busquedaObraEspecifica_view(request):
	usuario=infousuario.objects.get(user=request.user)
	if request.GET.get('Salir'):
		logout(request)
		return redirect('/')

	if request.GET.get('busqueda1'):
		return redirect('/BusquedaObraLiteraria')

	if request.GET.get('busqueda2'):
		return redirect('/BusquedaObraManualidad')

	if request.GET.get('busqueda3'):
		return redirect('/BusquedaObraMultimedia')

	return render(request,'BusquedaEspecifica.html')

@login_required(login_url='/')
def busquedaObraLiteraria_view(request):
	usuario=infousuario.objects.get(user=request.user)
	if request.GET.get('Salir'):
		logout(request)
		return redirect('/')

	return render(request,'BusquedaObraLiteraria.html')

@login_required(login_url='/')
def busquedaObraLiterariaResultado_view(request):
	usuario=infousuario.objects.get(user=request.user)
	if request.GET.get('Salir'):
		logout(request)
		return redirect('/')

	libros = infoLibro.objects.all()

	palabra = request.POST.get('buscarstring')
	print(palabra)

	librosPasan=[]
	pasanCombo = []

	if palabra is "" and not 'check1' in request.POST and not 'check2'in request.POST and not 'check3'in request.POST and not 'check4'in request.POST and not 'check5'in request.POST:
		return HttpResponse("No utilizó ninguna forma de búsqueda. Por favor vuelva a intentarlo.")

	if palabra is "":
		for libro in libros:
			if 'check1' in request.POST:
				if libro.genero.Comedia:
					librosPasan.append(libro)
			if 'check2' in request.POST:
				if libro.genero.Drama:
					librosPasan.append(libro)
			if 'check3' in request.POST:
				if libro.genero.Tragicomedia:
					librosPasan.append(libro)
			if 'check4' in request.POST:
				if libro.genero.Terror:
					librosPasan.append(libro)
			if 'check5' in request.POST:
				if libro.genero.Ciencia_Ficción:
					librosPasan.append(libro)

		if not librosPasan:
			context = {
				'librosPasan': librosPasan
			}
		else:
			count = Counter(librosPasan)
			count.most_common(1)[0][0]
			context = {
				'librosPasan': count
			}
		return render(request, 'BusquedaObraLiterariaResultado.html', context)

	for libro in libros:
		if palabra in libro.Titulo:
			librosPasan.append(libro)

	if not 'check1' in request.POST and not 'check2'in request.POST and not 'check3'in request.POST and not 'check4'in request.POST and not 'check5'in request.POST:
		if not librosPasan:
			context = {
				'librosPasan': librosPasan
			}
		else:
			count = Counter(librosPasan)
			count.most_common(1)[0][0]
			context = {
				'librosPasan': count
			}
		return render(request, 'BusquedaObraLiterariaResultado.html', context)

	for libro in librosPasan:
		if 'check1' in request.POST:
			if libro.genero.Comedia:
				pasanCombo.append(libro)
		if 'check2' in request.POST:
			if libro.genero.Drama:
				pasanCombo.append(libro)
		if 'check3' in request.POST:
			if libro.genero.Tragicomedia:
				pasanCombo.append(libro)
		if 'check4' in request.POST:
			if libro.genero.Terror:
				pasanCombo.append(libro)
		if 'check5' in request.POST:
			if libro.genero.Ciencia_Ficción:
				pasanCombo.append(libro)

	if not pasanCombo:
		context = {
			'librosPasan': pasanCombo
		}
	else:
		count = Counter(pasanCombo)
		count.most_common(1)[0][0]
		context = {
			'librosPasan': count
		}
	return render(request, 'BusquedaObraLiterariaResultado.html', context)

@login_required(login_url='/')
def busquedaObraManualidad_view(request):
	usuario=infousuario.objects.get(user=request.user)
	if request.GET.get('Salir'):
		logout(request)
		return redirect('/')

	return render(request,'BusquedaObraManualidad.html')

@login_required(login_url='/')
def busquedaObraManualidadResultado_view(request):
	usuario=infousuario.objects.get(user=request.user)
	if request.GET.get('Salir'):
		logout(request)
		return redirect('/')

	manualidades = contenidoManualidad.objects.all()

	palabra = request.POST.get('buscarstring')
	print(palabra)

	manualidadesPasan=[]
	pasanCombo = []

	if palabra is "" and not 'check1' in request.POST and not 'check2'in request.POST and not 'check3'in request.POST and not 'check4'in request.POST and not 'check5'in request.POST and not 'check6' in request.POST and not 'check7'in request.POST and not 'check8'in request.POST and not 'check9'in request.POST and not 'check10'in request.POST and not 'check11' in request.POST and not 'check12'in request.POST and not 'check13'in request.POST and not 'check14'in request.POST:
		return HttpResponse("No utilizó ninguna forma de búsqueda. Por favor vuelva a intentarlo.")

	if palabra is "":
		for manualidad in manualidades:
			if 'check1' in request.POST:
				if manualidad.genero.Bodegon:
					manualidadesPasan.append(manualidad)
			if 'check2' in request.POST:
				if manualidad.genero.Vanitas:
					manualidadesPasan.append(manualidad)
			if 'check3' in request.POST:
				if manualidad.genero.Retrato:
					manualidadesPasan.append(manualidad)
			if 'check4' in request.POST:
				if manualidad.genero.Terror:
					manualidadesPasan.append(manualidad)
			if 'check5' in request.POST:
				if manualidad.genero.Desnudo:
					manualidadesPasan.append(manualidad)
			if 'check6' in request.POST:
				if manualidad.genero.Religioso:
					manualidadesPasan.append(manualidad)
			if 'check7' in request.POST:
				if manualidad.genero.Historico:
					manualidadesPasan.append(manualidad)
			if 'check8' in request.POST:
				if manualidad.genero.Mitologico:
					manualidadesPasan.append(manualidad)
			if 'check9' in request.POST:
				if manualidad.genero.Paisaje:
					manualidadesPasan.append(manualidad)
			if 'check10' in request.POST:
				if manualidad.genero.Funeraria:
					manualidadesPasan.append(manualidad)
			if 'check11' in request.POST:
				if manualidad.genero.Monumento:
					manualidadesPasan.append(manualidad)
			if 'check12' in request.POST:
				if manualidad.genero.Estatuilla:
					manualidadesPasan.append(manualidad)
			if 'check13' in request.POST:
				if manualidad.genero.Figura:
					manualidadesPasan.append(manualidad)
			if 'check14' in request.POST:
				if manualidad.genero.Relieve:
					manualidadesPasan.append(manualidad)

		if not manualidadesPasan:
			context = {
				'manualidadesPasan': manualidadesPasan
			}
		else:
			count = Counter(manualidadesPasan)
			count.most_common(1)[0][0]
			context = {
				'manualidadesPasan': count
			}

		return render(request, 'BusquedaObraManualidadResultado.html', context)

	for manualidad in manualidades:
		if palabra in manualidad.title:
				manualidadesPasan.append(manualidad)

	if not 'check1' in request.POST and not 'check2'in request.POST and not 'check3'in request.POST and not 'check4'in request.POST and not 'check5'in request.POST and not 'check6' in request.POST and not 'check7'in request.POST and not 'check8'in request.POST and not 'check9'in request.POST and not 'check10'in request.POST and not 'check11' in request.POST and not 'check12'in request.POST and not 'check13'in request.POST and not 'check14'in request.POST:
		if not manualidadesPasan:
			context = {
				'manualidadesPasan': manualidadesPasan
			}
		else:
			count = Counter(manualidadesPasan)
			count.most_common(1)[0][0]
			context = {
				'manualidadesPasan': count
			}

		return render(request, 'BusquedaObraManualidadResultado.html', context)

	for manualidad in manualidadesPasan:
		if 'check1' in request.POST:
			if manualidad.genero.Bodegon:
				pasanCombo.append(manualidad)
		if 'check2' in request.POST:
			if manualidad.genero.Vanitas:
				pasanCombo.append(manualidad)
		if 'check3' in request.POST:
			if manualidad.genero.Retrato:
				pasanCombo.append(manualidad)
		if 'check4' in request.POST:
			if manualidad.genero.Terror:
				pasanCombo.append(manualidad)
		if 'check5' in request.POST:
			if manualidad.genero.Desnudo:
				pasanCombo.append(manualidad)
		if 'check6' in request.POST:
			if manualidad.genero.Religioso:
				pasanCombo.append(manualidad)
		if 'check7' in request.POST:
			if manualidad.genero.Historico:
				pasanCombo.append(manualidad)
		if 'check8' in request.POST:
			if manualidad.genero.Mitologico:
				pasanCombo.append(manualidad)
		if 'check9' in request.POST:
			if manualidad.genero.Paisaje:
				pasanCombo.append(manualidad)
		if 'check10' in request.POST:
			if manualidad.genero.Funeraria:
				pasanCombo.append(manualidad)
		if 'check11' in request.POST:
			if manualidad.genero.Monumento:
				pasanCombo.append(manualidad)
		if 'check12' in request.POST:
			if manualidad.genero.Estatuilla:
				pasanCombo.append(manualidad)
		if 'check13' in request.POST:
			if manualidad.genero.Figura:
				pasanCombo.append(manualidad)
		if 'check14' in request.POST:
			if manualidad.genero.Relieve:
				pasanCombo.append(manualidad)

	if not pasanCombo:
		context = {
			'manualidadesPasan': pasanCombo
		}
	else:
		count = Counter(pasanCombo)
		count.most_common(1)[0][0]
		context = {
			'manualidadesPasan': count
		}

	return render(request, 'BusquedaObraManualidadResultado.html', context)

@login_required(login_url='/')
def busquedaObraMultimedia_view(request):
	usuario=infousuario.objects.get(user=request.user)
	if request.GET.get('Salir'):
		logout(request)
		return redirect('/')

	return render(request,'BusquedaObraMultimedia.html')

@login_required(login_url='/')
def busquedaObraMultimediaResultado_view(request):
	usuario=infousuario.objects.get(user=request.user)
	if request.GET.get('Salir'):
		logout(request)
		return redirect('/')

	videos = contenidoMultimedia.objects.all()

	palabra = request.POST.get('buscarstring')
	print(palabra)

	videosPasan=[]
	pasanCombo = []

	if palabra is "" and not 'check1' in request.POST and not 'check2'in request.POST and not 'check3'in request.POST and not 'check4'in request.POST and not 'check5'in request.POST and not 'check6' in request.POST and not 'check7'in request.POST and not 'check8'in request.POST and not 'check9'in request.POST and not 'check10'in request.POST and not 'check11' in request.POST and not 'check12'in request.POST and not 'check13'in request.POST and not 'check14'in request.POST and not 'check15'in request.POST and not 'check16'in request.POST and not 'check17'in request.POST:
		return HttpResponse("No utilizó ninguna forma de búsqueda. Por favor vuelva a intentarlo.")

	if palabra is "":
		for video in videos:
			if 'check1' in request.POST:
				if video.genero.Comedia:
					videosPasan.append(video)
			if 'check2' in request.POST:
				if video.genero.Drama:
					videosPasan.append(video)
			if 'check3' in request.POST:
				if video.genero.Retrato:
					videosPasan.append(video)
			if 'check4' in request.POST:
				if video.genero.Terror:
					videoPasan.append(video)
			if 'check5' in request.POST:
				if video.genero.Accion:
					videosPasan.append(video)
			if 'check6' in request.POST:
				if video.genero.Belico:
					videosPasan.append(video)
			if 'check7' in request.POST:
				if video.genero.CienciaFiccion:
					videosPasan.append(video)
			if 'check8' in request.POST:
				if video.genero.Aventura:
					videosPasan.append(video)
			if 'check9' in request.POST:
				if video.genero.DelOeste:
					videosPasan.append(video)
			if 'check10' in request.POST:
				if video.genero.ArtesMarciales:
					videosPasan.append(video)
			if 'check11' in request.POST:
				if video.genero.Fantastico:
					videosPasan.append(video)
			if 'check12' in request.POST:
				if video.genero.Suspenso:
					videosPasan.append(video)
			if 'check13' in request.POST:
				if videos.genero.Historico:
					videosPasan.append(video)
			if 'check14' in request.POST:
				if video.genero.Adolescente:
					videosPasan.append(video)
			if 'check15' in request.POST:
				if video.genero.Infantil:
					videosPasan.append(video)
			if 'check16' in request.POST:
				if video.genero.Político_Social:
					videosPasan.append(video)
			if 'check17' in request.POST:
				if video.genero.Animacion:
					videosPasan.append(video)

		if not videosPasan:
			context = {
				'videosPasan': videosPasan
			}
		else:
			count = Counter(videosPasan)
			count.most_common(1)[0][0]
			context = {
				'videosPasan': count
			}

		return render(request, 'BusquedaObraMultimediaResultado.html', context)

	for video in videos:
		if palabra in video.title:
				videosPasan.append(video)

	if not 'check1' in request.POST and not 'check2'in request.POST and not 'check3'in request.POST and not 'check4'in request.POST and not 'check5'in request.POST and not 'check6' in request.POST and not 'check7'in request.POST and not 'check8'in request.POST and not 'check9'in request.POST and not 'check10'in request.POST and not 'check11' in request.POST and not 'check12'in request.POST and not 'check13'in request.POST and not 'check14'in request.POST and not 'check15'in request.POST and not 'check16'in request.POST and not 'check17'in request.POST:
		if not videosPasan:
			context = {
				'videosPasan': videosPasan
			}
		else:
			count = Counter(videosPasan)
			count.most_common(1)[0][0]
			context = {
				'videosPasan': count
			}

		return render(request, 'BusquedaObraMultimediaResultado.html', context)

	for video in videosPasan:
		if 'check1' in request.POST:
			if video.genero.Comedia:
				pasanCombo.append(video)
		if 'check2' in request.POST:
			if manualidad.genero.Drama:
				pasanCombo.append(video)
		if 'check3' in request.POST:
			if video.genero.Retrato:
				pasanCombo.append(video)
		if 'check4' in request.POST:
			if video.genero.Terror:
				pasanCombo.append(video)
		if 'check5' in request.POST:
			if video.genero.Accion:
				pasanCombo.append(video)
		if 'check6' in request.POST:
			if video.genero.Belico:
				pasanCombo.append(video)
		if 'check7' in request.POST:
			if video.genero.CienciaFiccion:
				pasanCombo.append(video)
		if 'check8' in request.POST:
			if video.genero.Aventura:
				pasanCombo.append(video)
		if 'check9' in request.POST:
			if video.genero.DelOeste:
				pasanCombo.append(video)
		if 'check10' in request.POST:
			if video.genero.ArtesMarciales:
				pasanCombo.append(video)
		if 'check11' in request.POST:
			if video.genero.Fantastico:
				pasanCombo.append(video)
		if 'check12' in request.POST:
			if video.genero.Suspenso:
				pasanCombo.append(video)
		if 'check13' in request.POST:
			if videos.genero.Historico:
				pasanCombo.append(video)
		if 'check14' in request.POST:
			if video.genero.Adolescente:
				pasanCombo.append(video)
		if 'check15' in request.POST:
			if video.genero.Infantil:
				pasanCombo.append(video)
		if 'check16' in request.POST:
			if video.genero.Político_Social:
				pasanCombo.append(video)
		if 'check17' in request.POST:
			if video.genero.Animacion:
				pasanCombo.append(video)

	if not pasanCombo:
		context = {
			'videosPasan': pasanCombo
		}
	else:
		count = Counter(pasanCombo)
		count.most_common(1)[0][0]
		context = {
			'videosPasan': count
		}

	return render(request, 'BusquedaObraManualidadResultado.html', context)
