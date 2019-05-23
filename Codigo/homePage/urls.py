from django.conf.urls import url
from . import views
from django.conf import settings
from django.urls import path
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns=[

	url(r'^$', views.index, name='Home Page'),
	url(r'^Registro$', views.registro_view, name='JaveCultura Registro Page'),
	url(r'^HomePage$', views.homePage_view, name='Home Page'),
	url(r'^CatalogoLibros$',views.libros_view, name='catalogo libros'),
	url(r'^CatalogoMultimedia$',views.multimedia_view, name='catalogo Videos'),
	url(r'^CatalogoManualidades$',views.manualidad_view, name='catalogo Manualidad'),
	url(r'^Perfil$',views.perfil_view,name='perfil'),
	url(r'^CompraCredito$', views.comprarCredito_view, name='comprar credito'),
	url(r'^SubirObra$', views.subirObra_view, name='Seleccion de tipo de Obra'),
	url(r'^VistaComprados$', views.comprados_view, name='ver comprados'),
	url(r'^VistaCompradores$', views.compradores_view, name='ver compradores'),
	url(r'^CarritoVista$', views.carrito_view, name='ver carrito'),
	url(r'^VistaDonantes$', views.donadores_view, name='ver Donadores'),
	url(r'^AquienDone$', views.AquienDone_view, name='ver a quien done'),
	url(r'^SubirObra/SubirContenidoLiterario$', views.subirObraLiteraria_view, name='Subir contenido literario'),
	url(r'^SubirContenidoMultimedia$',views.SubirContenidoMultimedia_view,name='Subir contenido multimedia'),
	url(r'^SubirManualidad$', views.subirManualidades_view, name='Subir contenido Manual'),
	url(r'^BusquedaColaboradores$', views.busquedaColaboradores_view, name='Busqueda de colaboradores'),
	url(r'^BusquedaColaboradoresResultado$', views.busquedaColaboradoresResultado_view, name='Busqueda de colaboradoresR'),
	url(r'^BusquedaGeneral$', views.busquedaObraGeneral_view, name='Busqueda general de obras'),
	url(r'^BusquedaEspecifica$', views.busquedaObraEspecifica_view, name='Busqueda especifica de obras'),
	url(r'^BusquedaObraLiteraria$', views.busquedaObraLiteraria_view, name='Busqueda de obra literaria'),
	url(r'^BusquedaObraManualidad$', views.busquedaObraManualidad_view, name='Busqueda de manualidad'),
	url(r'^BusquedaObraMultimedia$', views.busquedaObraMultimedia_view, name='Busqueda de multimedia'),
	url(r'^BusquedaObraLiterariaResultado$', views.busquedaObraLiterariaResultado_view, name='Busqueda de obra literariaR'),
	url(r'^BusquedaObraManualidadResultado$', views.busquedaObraManualidadResultado_view, name='Busqueda de manualidadR'),
	url(r'^BusquedaObraMultimediaResultado$', views.busquedaObraMultimediaResultado_view, name='Busqueda de multimediaR'),
	path('EditarUsuario', views.editarUsuarioInfo),
	path ('Contacto', views.vistaContactos),
	path('Producto/ContenidoLiterario/Comentar/<int:primaryKey>', views.comentarios_calificacionLibro),
	path('Producto/ContenidoManualidad/Editar/<int:primaryKey>', views.editarManualidades_view),
	path('Producto/ContenidoLiterario/Editar/<int:primaryKey>', views.editarContenidoLiterario_view),
	path('Producto/ContenidoMultimedia/Editar/<int:primaryKey>', views.editarMultimedia_view),
	path('VistaVideo/<int:primaryKey>', views.video_View),
	path('VistaUsuario/Usuario/<int:primaryKey>', views.mostrarUsuario),
	path('Producto/ContenidoMultimedia/<int:primaryKey>', views.mostrarMultimedia),
	path('Producto/ContenidoLiterario/<int:primaryKey>', views.mostrarObraLiteraria),
	path('VistaUsuario/Usuario/Donacion/<int:primaryKey>', views.Donacion_view),
	path('VistaUsuario/Usuario/Contratar/<int:primaryKey>', views.contratar_view),
	path('Producto/ContenidoManualidad/<int:primaryKey>', views.mostrarManualidad),
	path('Producto/ContenidoManualidad/Comentar/<int:primaryKey>', views.comentarios_calificacionManu),
	path('EnviarMensaje/<int:primaryKey>', views.EnviarMensaje),
	path('BandejaEntrada', views.bandejaView),
	path('BandejaEntrada/<int:primaryKey>', views.mensajeView),
	path('BandejaContrato', views.bandejaContrato_view),
	path('BandejaContrato/<int:primaryKey>', views.contrato_view),
	path('Producto/ContenidoManualidad/Comentar/<int:primaryKey>', views.comentarios_calificacionManu),
	path('ActivarCuenta/<int:codigo>',views.activarCueta_view),
	path('CerrarCuenta',views.cerrarCuenta_view),
# Create your views here.
		]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
