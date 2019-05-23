from django.core.mail import send_mail
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
from datetime import date
import os
from django.contrib import messages


def establecerContacto(usuario1, usuario2):
	if len(Contactos.objects.filter(Activo=usuario1, Pasivo=usuario2) )== 0 :
		Contactos.objects.create(Pasivo=usuario2, Activo=usuario1)
		Contactos.objects.create(Activo=usuario2, Pasivo=usuario1)

@login_required(login_url='/')
def vistaContactos(request):
	if request.GET.get('Salir'):
		logout(request)
		return redirect('/')

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
				print("ava",url)
				return redirect(url)
	return render(request,'verContactos.html',{'infoContactos':infoContactos,'hayContactos':hayContactos})

@login_required(login_url='/')
def EnviarMensaje(request, primaryKey):
	if request.GET.get('Salir'):
		logout(request)
		return redirect('/')

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
			msj="Mensaje enviado con exito"
			return render(request,'HomePage.html',{'msj':msj})
		#end if
	else:
		form=MensajeForm()
	#end else
	return render(request,'EnviarMensaje.html',{'Form':form})


@login_required(login_url='/')
def bandejaView (request):

	if request.GET.get('Salir'):
		logout(request)
		return redirect('/')

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
def video_View(request, primaryKey):

	if request.GET.get('Salir'):
		logout(request)
		return redirect('/')

	video=contenidoMultimedia.objects.get(pk=primaryKey)
	if video is not None:
		return render(request, 'visualizarVideo.html',{'video':video})
	else:
		raise Http404


@login_required(login_url='/')
def mensajeView(request, primaryKey):

	if request.GET.get('Salir'):
		logout(request)
		return redirect('/')

	Mensaje=Mensajes.objects.get(pk=primaryKey, Receptor=request.user)
	if request.GET.get('responder'):
		return redirect('/EnviarMensaje/'+str(Mensaje.Emisor.pk))
	if Mensaje is not None:
		return render(request, 'visualizarMensaje.html',{'Mensaje':Mensaje})
	else:
		raise Http404

@login_required(login_url='/')
def contratar_view(request, primaryKey):

	if request.GET.get('Salir'):
		logout(request)
		return redirect('/')

	if request.method =='POST' or request.method =='GET':
		Contrato_Form = ContratoForm(request.POST)
		if Contrato_Form.is_valid():

			auxEmisor = infousuario.objects.get(user=request.user)
			auxReceptor = infousuario.objects.get(pk=primaryKey)
			msj =None
			if auxReceptor.es_Colaborador:
				data = Contrato_Form.cleaned_data
				salario = data.get("valorOfrecido")
				titulo = data.get("Titulo")
				mensaje = data.get("Cuerpo")

				if auxEmisor.balance >= salario:
					contrato = Contrato.objects.create(valorOfrecido = salario, Emisor = auxEmisor.user, Receptor = auxReceptor.user, Titulo = titulo, Cuerpo = mensaje)
					auxEmisor.balance = auxEmisor.balance - salario
					auxEmisor.save()
					msj = "Contrato enviado"
					return render(request,'Contratar.html',{'Receptor':infousuario.objects.get(pk=primaryKey),'Contrato_Form':Contrato_Form, 'msj':msj })
				else:
					return redirect('/CompraCredito')
			else:
				msj="El usuario al que desea contratar no es se ha confirmado como colaborador. Por favor busque a alguien más"
				return render(request,'Contratar.html',{'Receptor':infousuario.objects.get(pk=primaryKey),'Contrato_Form':Contrato_Form, 'msj':msj })
				
		else:
			Contrato_Form = ContratoForm()

	return render(request,'Contratar.html',{'Receptor':infousuario.objects.get(pk=primaryKey),'Contrato_Form':Contrato_Form})

@login_required(login_url='/')
def bandejaContrato_view (request):

	if request.GET.get('Salir'):
		logout(request)
		return redirect('/')

	hayContratos = True
	contratosRecibidos=Contrato.objects.order_by('-fecha').filter(Receptor=request.user)
	for contratoDado in contratosRecibidos:
			aux1 = str(contratoDado.pk)
			aux1 = aux1.strip()
			if request.GET.get(aux1) is not None:
				contratoDado.delete()
				return redirect('/BandejaContrato')
	if not contratosRecibidos:
		hayContratos = False
	return render(request, 'BandejaContrato.html',{'contratos':contratosRecibidos, 'hayContratos':hayContratos})

@login_required(login_url='/')
def contrato_view(request, primaryKey):

	if request.GET.get('Salir'):
		logout(request)
		return redirect('/')
	contrato = Contrato.objects.get(pk=primaryKey, Receptor=request.user)
	msj = None
	if request.GET.get('aceptar'):
		establecerContacto(contrato.Emisor, contrato.Receptor)
		auxReceptor = infousuario.objects.get(user = contrato.Receptor)
		auxReceptor.balance = auxReceptor.balance + contrato.valorOfrecido
		auxReceptor.save()
		contrato.delete()
		msj = "El contrato ha sido aceptado. Se ha añadido al usuario a sus lista de contactos."
		return render(request, 'contrato.html',{'contrato': contrato, 'msj':msj})

	if request.GET.get('rechazar'):
		auxEmisor = infousuario.objects.get(user = contrato.Emisor)
		auxEmisor.balance = auxEmisor.balance + contrato.valorOfrecido
		auxEmisor.save()
		contrato.delete()
		return redirect('/BandejaContrato')

	if contrato is not None:
		return render(request, 'contrato.html',{'contrato': contrato})
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
		#----------------------------------------------------------------------------------

			sesionPotencial= User.objects.get(username =nombreUsuario)
			print("Cuenta cerrada? "+ str(infousuario.objects.get(user =sesionPotencial).cuantaCerrada)  )
			if infousuario.objects.get(user =sesionPotencial).cuantaCerrada:
			    msj="La cuenta de la que está tratando de acceder esta cerrada"
			    return render(request, 'paginaInicio.html',{'form':form,"msj":msj})
			if infousuario.objects.get(user =sesionPotencial).tieneCuentaActivada:
				login(request,acceso)
				return redirect('/')#TODO: return pagina de inicio despues de iniciar sesion
			else:
				msj="La cuenta todavia no ha sido activada, por favor revisar correo"
				return render(request, 'paginaInicio.html',{'form':form,"msj":msj})


		#-------------------------------------------------------------------------------------n redirect('/HomePage')#TODO: return pagina de inicio despues de iniciar sesion
		else:
			msj="Usuario o contraseña no coincide/existe"
			return render(request, 'paginaInicio.html',{'form':form,"msj":msj})
	else:
		form=logInForm()
	return render(request, 'paginaInicio.html',{'form':form})
# Create your views here.

#--------------------------------------------Activar cuenta
def activarCueta_view(request,codigo):
	idcuenta=codigo/12345
	aux=infousuario.objects.get(pk=idcuenta)
	aux.tieneCuentaActivada=True
	aux.save()
	msj="Su cuenta ha sido Activada con exito"
	return render(request, 'paginaInicio.html',{'form':form,"msj":msj})
#----------------------------------------------

def registro_view(request):
	if request.method =='POST':
		Competencias_Form=competenciasForm(request.POST)
		User_Form= RegistroForm(request.POST)
		Info_Form=infoForm(request.POST,request.FILES)
		if User_Form.is_valid() and Info_Form.is_valid():
			#---------------------------------------------------
			user=User_Form.save(commit=False)
			competencias=Competencias_Form.save(commit=False)
			profile=Info_Form.save(commit=False)
			#---------------------------------------------------
			profile.aficiones=competencias
			profile.user=user
			#-------------------------------------------------
			profile.tieneCuentaActivada=False
			profile.cuentaCerrada=False
			if profile.es_CreadorDeContenido :
				if "@javeriana.edu.co" in profile.user.email:
					print('pass')
				else:
					msj="Para ser creador de contenido debes poner un correo de extension @javeriana.edu.co"
					return render(request,'Registro.html', {'competencias_Form':Competencias_Form,'user_form':User_Form, 'profile_form':Info_Form,'msj':msj})
			user.save()
			competencias.save()
			profile.aficiones=competencias
			profile.user=user
			#-------------------------------------------
			profile.save()
			#Enviar correo de confirmacion----------------------------------------------
			subject="Zona Cultura: Correo de confirmacion"
			message="¡Bienvenido a nuestra comunidad! Para confirmar su cuenta porfavor ir a la pagina: \n"+"http://schaparrop.pythonanywhere.com/ActivarCuenta/"+str(profile.pk*12345)
			from_email= settings.EMAIL_HOST_USER
			to_list=[user.email,'santiagochaparro@javeriana.edu.co']
			send_mail(subject, message, from_email, to_list,fail_silently=False)
			#Enviar correo de confirmacion fin---------------------------------------------
			return render(request,'revisarCorreoPorFavor.html')
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
	if request.GET.get('editarperfil'):
		return redirect('/EditarUsuario')
	if request.GET.get('NoserColaborador'):
		user.es_Colaborador= False
		user.save()
		return redirect('/Perfil')
	if request.GET.get('Mensajes'):
		return redirect('/Contacto')
	if request.GET.get('Contacto'):
		return redirect('/BandejaEntrada')
	if request.GET.get('cerrarcuenta'):
		return redirect('/CerrarCuenta')
	if request.GET.get('Contratos'):
		return redirect('/BandejaContrato')
	return render(request, 'PerfilPropio.html',{'user':user})





@login_required(login_url='/')
def cerrarCuenta_view(request):

	if request.GET.get('Salir'):
		logout(request)
		return redirect('/')

	if request.GET.get('Si'):
		aux=infousuario.objects.get(user=request.user)
		aux.cuantaCerrada=True
		aux.save()
		logout(request)
		return redirect('/')
	if request.GET.get('No'):
		return redirect('/Perfil')
	return render(request,'cerrarcuenta.html')
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
def manualidad_view(request):
	manualidad=contenidoManualidad.objects.all()
	contexto={'manualidad':manualidad}
	return render(request,'catalogoMultimedia.html',contexto)
@login_required(login_url='/')
def subirObra_view (request):

	if request.GET.get('Salir'):
		logout(request)
		return redirect('/')

	return render(request,'SubirObra.html');

@login_required(login_url='/')
def subirObraLiteraria_view(request):

	if request.GET.get('Salir'):
		logout(request)
		return redirect('/')

	if request.method =='POST':
		Form=contenidoLiterarioForm(request.POST, request.FILES)
		Form2=generoLiterarioForm(request.POST)
		if Form.is_valid():
			generos=Form2.save()
			producto=Form.save(commit=False)
			print(str(producto.archivo))
			if str(producto.archivo) =='contenido/books/default.pdf':
				msj="Error, tiene que subir obligatoriamente un archivo pdf para vender la obra"
				return render(request,'SubirContenidoLiterario.html',{'Form':Form,'Form2':Form2,'msj':msj})
			producto.user= request.user
			producto.genero=generos
			producto.save()
			print("\n***********Formulario valido")
			print("Obra",producto.Titulo," subida, y le quedo una llave primaria de:", producto.id)

			return HttpResponse("Submited")
		else:
			print("\n***********Formulario no valido")
			msj="Error, datos incorrectos en el formulario"
			return render(request,'SubirContenidoLiterario.html',{'Form':Form,'Form2':Form2,'msj':msj})
	else:
		Form2=generoLiterarioForm()
		Form=contenidoLiterarioForm()
	return render(request,'SubirContenidoLiterario.html',{'Form':Form,'Form2':Form2})
@login_required(login_url='/')
def mostrarObraLiteraria(request,primaryKey):
	#allObjects=infoLibro.objects.all()
	#print([p.pk for p in allObjects])
	print(primaryKey)
	permitir2=True
	mostrarBotonCarrito=True
	try:
		Libro=infoLibro.objects.get(pk=primaryKey)



		if(ArticulosComprados.objects.filter(usuario=infousuario.objects.get(user = request.user),libro=Libro).first() is not None):
			permitir2=False
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
		c=Carrito.objects.filter(libro=Libro,usuario=infousuario.objects.get(user=request.user)).first()
		if c is not None:
			permitir2=False
		if request.GET.get('carrito'):
			print('Hello! el libro con id: ',Libro.id)
			print(c)
			if c is None :
				carro=Carrito.objects.create(libro= Libro, usuario=infousuario.objects.get(user=request.user))
				return redirect('/CarritoVista')
			else:

				mostrarBotonCarrito=False


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
	return render(request, 'mostrarContentidoLiterario.html',{'User':request.user,'Libro':Libro,'generos':aux, 'permitir':permitir, 'hayComentarios':hayComentarios, 'comentarios':comentarios, 'promedioCalificacion':promedioCalificacion, 'mostrarBotonCarrito':mostrarBotonCarrito, 'permitir2':permitir2})


@login_required(login_url='/')
def mostrarMultimedia(request,primaryKey):
	#allObjects=infoLibro.objects.all()
	#print([p.pk for p in allObjects])
	if request.GET.get('Salir'):
		logout(request)
		return redirect('/')

	print(primaryKey)


	try:
		video=contenidoMultimedia.objects.get(pk=primaryKey)



		if(ArticulosComprados.objects.filter(usuario=infousuario.objects.get(user = request.user),multimedia=video).first() is not None):
			permitir=False
			print('lo tiene')
		else:
			permitir=True
			print('no lo tiene')
		if request.GET.get('ver'):
			return redirect('/')

		if request.GET.get('carrito'):
			print('Hello! el vvibro con id: ',video.id)
			c=Carrito.objects.filter(multimedia=video,usuario=infousuario.objects.get(user=request.user)).first()
			print(c)
			if c is None :
				carro=Carrito.objects.create(multimedia= video, usuario=infousuario.objects.get(user=request.user))
				return redirect('/CarritoVista')
			else:
				return HttpResponse("Usted ya tiene este elemento en el carrito")
			#carro.usuario=infousuario.objects.get(user=request.user)
			#print("Usuario:",infousuario.objects.get(user=request.user).id)
	except:
		print('pppp')
		raise Http404
	listaDeGeneros= video.genero
	print(listaDeGeneros)
	aux=''
	if listaDeGeneros.Comedia==True :
		print('Es de Comedia')
		aux=aux+'Comedia'
	if listaDeGeneros.Drama==True :
		aux=aux+'Drama'
	if listaDeGeneros.Retrato==True :
		aux=aux+'Retrato '
	if listaDeGeneros.Terror==True :
		aux=aux+'Terror '
	if listaDeGeneros.CienciaFiccion==True :
		aux=aux+'Ciencia Ficción '
	if listaDeGeneros.Accion==True :
		aux=aux+'Accion'
	if listaDeGeneros.Belico==True :
		aux=aux+'Belico'
	if listaDeGeneros.Aventura==True :
		aux=aux+'Aventura'
	if listaDeGeneros.DelOeste==True :
		aux=aux+'DelOeste'
	if listaDeGeneros.ArtesMarciales==True :
		aux=aux+'Artes Marciales'
	if listaDeGeneros.Fantastico==True :
		aux=aux+'Fantastico'
	if listaDeGeneros.Suspenso==True :
		aux=aux+'Suspenso'
	if listaDeGeneros.Historico==True :
		aux=aux+'Historico'
	if listaDeGeneros.Adolescente==True :
		aux=aux+'Adolescente'
	if listaDeGeneros.Infantil==True :
		aux=aux+'Infantil'
	if listaDeGeneros.Político_Social==True :
		aux=aux+'Político Social'
	if listaDeGeneros.Animacion==True :
		aux=aux+'Animacion'
	comentarios=ComentarioMultimedia.objects.filter(video=video)
	hayComentarios=True
	promedioCalificacion=0
	if len(comentarios)== 0:
		hayComentarios=False
	else:
		for comentario in comentarios:
			promedioCalificacion=promedioCalificacion+comentario.califi
		promedioCalificacion=promedioCalificacion/len(comentarios)
	return render(request, 'mostrarContenidoMultimedia.html',{'User':request.user,'video':video,'generos':aux, 'permitir':permitir, 'hayComentarios':hayComentarios, 'comentarios':comentarios, 'promedioCalificacion':promedioCalificacion})




@login_required(login_url='/')
def comprarCredito_view(request):

	if request.GET.get('Salir'):
		logout(request)
		return redirect('/')

	msj=None
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
												msj="La tarjeta es valida pero ya esta vencida"
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
				msj="Comprado"
			else:
				msj="La tarjeta no existe o ingreso algún campo erroneo"

			#return redirect('/')
	else:
		Card_Form =contenidoTarjetaForm()
		Credit_Form =contenidoCreditForm()

	return render(request,'CompraCredito.html',{'card_Form':Card_Form,'credit_Form':Credit_Form,'msj':msj})

@login_required(login_url='/')
def carrito_view(request):
	if request.GET.get('Salir'):
		logout(request)
		return redirect('/')
	mjs=None
	usuario= infousuario.objects.get(user = request.user)
	libros=[]
	manualidades=[]
	multimedias=[]
	carri=Carrito.objects.filter(usuario= infousuario.objects.get(user = request.user))
	cantidad=0
	for item in carri:
		if( item.libro is not None):#Si es un libro
			libros.append(item.libro)
			cantidad=cantidad+1
		if( item.manualidad is not None):
			manualidades.append(item.manualidad)
			cantidad=cantidad+1
		if( item.multimedia is not None):
			multimedias.append(item.multimedia)
			cantidad=cantidad+1

	total=0

	#Sacar total libros

	for p in libros:
		total=total+p.PrecioLibro

	for m in manualidades:
		if(m.existencias!=0):
			total=total+m.precioV
	for v in multimedias:
			total=total+v.precioV
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
                for v in multimedias:
                    r=infousuario.objects.get(user=v.user)
                    r.balance=r.balance+v.precioV

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
                        establecerContacto(item.manualidad.user,request.user)
                        item.manualidad.existencias=item.manualidad.existencias-1
                        item.manualidad.save()
                        Compradores.objects.create(manualidad=item.manualidad,usuarioDuenio=usuarioDd,usuarioComprador=usuario)
                        item.delete()
                        cantidad=cantidad-1
                    if(item.multimedia is not None ):
                        ArticulosComprados.objects.create(multimedia= item.multimedia, usuario=usuario)#esto va a cambiar cuando agregemos multimedia y manualidades
                        usuarioDd= infousuario.objects.get(user =item.multimedia.user)
                        item.multimedia.save()
                        Compradores.objects.create(multimedia=item.multimedia,usuarioDuenio=usuarioDd,usuarioComprador=usuario)
                        item.delete()
                        cantidad=cantidad-1
                    print("hola cssantidad")
                    print(cantidad)
                if(cantidad!=0):
                    print("hola cantidad")
                    print(cantidad)
                    mjs="No se pudieron comprar todas las unidades, verifique las existencias del producto"
					#return HttpResponse("No se pudieron comprar todos los elemntos, verifique quizás las existencias del articulo se agotaron ")
                else:

                    auxi=1
                    if(auxi==1):
                       return redirect('/CarritoVista')
            else:
            	mjs="Usted no posee credito suficiente "
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
		for video in multimedias:
			aux2="Video"+str(video.pk)
			aux2=aux2.strip()
			if request.GET.get(aux2) is not None:
				print('Encontro articulo')
				carr=Carrito.objects.filter(multimedia=video,usuario=usuario)
				carr[0].delete()
				return redirect('/CarritoVista')


	#print("Total ",total )
	#print([p.Titulo for p in libros])
	return render(request,'CarritoVista.html',{'libros':libros, 'manualidades': manualidades,'multimedias':multimedias,'Subtotal': total,'carrito':carri,'mjs':mjs})
@login_required(login_url='/')
def comprados_view(request):

	if request.GET.get('Salir'):
		logout(request)
		return redirect('/')

	usuario= infousuario.objects.get(user = request.user)
	libros=[]
	manualidades=[]
	infix=None
	comprados =ArticulosComprados.objects.filter(usuario= infousuario.objects.get(user = request.user))
	for item in comprados:
		if( item.libro is not None):#Si es un libro
			libros.append(item.libro)
		if( item.manualidad is not None):#Si es un libro
			manualidades.append(item.manualidad)
			print("contacto ok")
			infix=item.manualidad.user
			aux1=""+str(infix.pk)
			aux1=aux1.strip()
			#print(aux1)
			if request.GET.get(aux1) is not None:
				print('Encontro articulo')
				url= '/EnviarMensaje/'+aux1
				print("ava",url)
				return redirect(url)




	return render(request,'VistaComprados.html',{'libros':libros,'manualidades':manualidades,'infix':infix})
@login_required(login_url='/')
def compradores_view(request):

	if request.GET.get('Salir'):
		logout(request)
		return redirect('/')

	usuario= infousuario.objects.get(user = request.user)
	usuariosCompradores=[]
	usuariosCompraManu=[]
	usuariosCompraVid=[]
	compradxres=Compradores.objects.filter(usuarioDuenio=infousuario.objects.get(user = request.user))
	for item in compradxres:
		if( item.usuarioComprador is not None and item.libro is not None ):#Si es un libro
			usuariosCompradores.append(item)
		if( item.usuarioComprador is not None and item.manualidad is not None ):#Si es un libro
			usuariosCompraManu.append(item)
		if( item.usuarioComprador is not None and item.multimedia is not None ):#Si es un libro
			usuariosCompraVid.append(item)

	return render(request,'VistaCompradores.html',{'usuariosCompradores':usuariosCompradores,'usuariosCompraManu':usuariosCompraManu,'usuariosCompraVid':usuariosCompraVid})






@login_required(login_url='/')
def Donacion_view(request,primaryKey):
	msj=None
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
					msj="Donacion satisfactoria"
				else:
					return redirect('/CompraCredito')
			else:
				msj="El usuario al que desea donar no es creador de contenido, si desea donar por favor busque un creador de contenido"




	else:
		Donacion_Form=DonacionForm()

	return render(request,'VistaDonacion.html',{'UsuariBeni':infousuario.objects.get(pk=primaryKey),'Donacion_Form':Donacion_Form,'msj':msj})
@login_required(login_url='/')
def mostrarUsuario(request,primaryKey):
	try:
		Usu=infousuario.objects.get(pk=primaryKey)
		if request.GET.get('contratar'):
			return redirect('/VistaUsuario/Usuario/Contratar/'+Usu.pk)
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


def SubirContenidoMultimedia_view(request):
    if request.method=='POST':
        multimedia_form=contenidoMultimediaForm(request.POST, request.FILES)
        multimedia_form2=GeneroMultimediaForm(request.POST)
        if multimedia_form.is_valid():
            generos=multimedia_form2.save()
            producto=multimedia_form.save(commit=False)
            producto.user=request.user
            producto.genero=generos
            producto.save()
            return HttpResponse("Submited")
        else:
            print("\n***********Formulario no valido")
            mens="Fallo"
            return HttpResponse("Fallo")
    else:
        multimedia_form=contenidoMultimediaForm()
        multimedia_form2=GeneroMultimediaForm()
    return render(request,'SubirVideo.html',{'multimedia_form': multimedia_form, 'multimedia_form2':multimedia_form2})
@login_required(login_url='/')
def subirManualidades_view(request):
	mens=None
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

			mens="Subida con éxito"
		else:
			print("\n***********Formulario no valido")
			mens="Fallo"
	else:

		Form2=GeneroManualidadForm()
		Form=contenidoManualForm()
	return render(request,'SubirManualidad.html',{'Form':Form,'Form2':Form2,'mens':mens})

@login_required(login_url='/')
def mostrarManualidad(request,primaryKey):
	#allObjects=infoLibro.objects.all()
	#print([p.pk for p in allObjects])
	mensjj=None
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
				mensjj="No se pudo añadir"

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

	return render(request, 'mostrarManualidad.html' ,{'Manualidad':Manualidad,'com':com,'usuario':usuario,'generos':aux,'mensjj':mensjj})

@login_required(login_url='/')
def editarManualidades_view(request,primaryKey):
	mensjj=None
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

			mensjj="Submited"
		else:
			Form = EmpleadoForm(instance=Manualidad)
			print("\n***********Formulario no valido")
			mensjj="Fallo"
	else:
		Form2=GeneroManualidadForm(instance=Manualidad.genero)
		Form=contenidoManualForm(instance=Manualidad)

	return render(request,'EditarManualidad.html',{'Form':Form,'Form2':Form2,'mensjj':mensjj})


@login_required(login_url='/')
def comentarios_calificacionLibro(request,primaryKey):
	mensaje=None
	Libro=infoLibro.objects.get(pk=primaryKey)
	usu = infousuario.objects.get(user = request.user)

	aux=ArticulosComprados.objects.filter(usuario=usu, libro=Libro)
	aux2= ComentarioObraLiteraria.objects.filter(usuarioComentador=usu, libro=Libro)
	if len(aux2)==0:
		if  len(aux) >0:
			if request.method =='POST':
				if(Libro.user.username==usu.user.username):
					mensaje="No puede comentar su propia obra"
				else:
					com= comenycaliFormLibro(request.POST)
					if com.is_valid():
						comentario=com.save(commit=False)
						comentario.libro=Libro
						comentario.usuarioComentador=usu
						comentario.save()
						print("\n***********Formulario valido")
						mensaje="Comentario enviado"
					#return redirect('/')
			else:
				com = comenycaliFormLibro()
		else:
			raise Http404
	else:
		raise Http404
	return render(request,'comentarLibro.html',{'com':com,'Libro':Libro,'mensaje':mensaje})

@login_required(login_url='/')
def comentarios_calificacionManu(request,primaryKey):
	M=None
	com=None

	Manualidad=contenidoManualidad.objects.get(pk=primaryKey)
	usu = infousuario.objects.get(user = request.user)

	if request.method =='POST':
		if(Manualidad.user.username==usu.user.username):
			M="No puede comentar su propia obra"
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
				M="Comentario enviado"
			#return redirect('/')
	else:
		com =comenycaliForm()

	return render(request,'comentarManu.html',{'com':com,'Manualidad':Manualidad,'M':M})

@login_required(login_url='/')
def editarContenidoLiterario_view(request,primaryKey):
	Libro=infoLibro.objects.get(pk=primaryKey)
	if Libro.user.pk != request.user.pk:
		raise Http404
	else:
		if request.method =='POST':
			Form=contenidoLiterarioForm(request.POST, request.FILES,instance=Libro)
			Form2=generoLiterarioForm(request.POST,instance=Libro.genero)
			if Form.is_valid():
				generos=Form2.save()
				producto=Form.save(commit=False)

				if str(producto.archivo) =='contenido/books/default.pdf':
					msj="Error, tiene que subir obligatoriamente un archivo pdf para vender la obra"
					return render(request,'SubirContenidoLiterario.html',{'Form':Form,'Form2':Form2,'msj':msj})
				producto.user= request.user
				producto.genero=generos
				producto.save()

				print("Obra",producto.Titulo," subida, y le quedo una llave primaria de:", producto.pk)

				return HttpResponse("Submited")
			else:
				msj="Error en los datos del formulario"
				return render(request,'EditarManualidad.html',{'Form':Form,'Form2':Form2,'msj':msj})
		else:
			Form=contenidoLiterarioForm(instance=Libro)
			Form2=generoLiterarioForm(instance=Libro.genero)

		return render(request,'EditarManualidad.html',{'Form':Form,'Form2':Form2})
def editarMultimedia_view(request,primaryKey):
    mensjj=None
    video=contenidoMultimedia.objects.get(pk=primaryKey)
    if video.user.pk != request.user.pk: ##LO AGREGO SANTIAGO
        raise Http404
    if request.method=='POST':
        multimedia_form=contenidoMultimediaForm(request.POST, request.FILES,instance=video)
        multimedia_form2=GeneroMultimediaForm(request.POST,instance=video.genero)
        if multimedia_form.is_valid():
            generos=multimedia_form2.save()
            producto=multimedia_form.save(commit=False)
            producto.user=request.user
            producto.genero=generos
            producto.save()
            mensjj="Submited"
        else:
            print("\n***********Formulario no valido")
            mens="Fallo"
            return HttpResponse("Fallo")
    else:
        multimedia_form=contenidoMultimediaForm(instance=video)
        multimedia_form2=GeneroMultimediaForm(instance=video.genero)
    return render(request,'EditarContenidoMultimedia.html',{'Form':multimedia_form,'Form2':multimedia_form2,'mensjj':mensjj})

@login_required(login_url='/')
def editarUsuarioInfo(request):
	#asegurarse que el usuario sea el mismo
	usuario=infousuario.objects.get(user=request.user)
	if request.method =='POST':
		Form=RegistroForm2(request.POST,instance=usuario.user)
		Form2=competenciasForm(request.POST,instance=usuario.aficiones)
		Form3=infoForm2(request.POST,request.FILES,instance=usuario)
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
		Form=RegistroForm2(instance=usuario.user)
		Form2=competenciasForm(instance=usuario.aficiones)
		Form3=infoForm2(instance=usuario)
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
