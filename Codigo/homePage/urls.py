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
	url(r'^SubirObra$', views.subirObra_view, name='Seleccion de tipo de Obra'),
	url(r'^SubirObra/SubirContenidoLiterario$', views.subirObraLiteraria_view, name='Subir contenido literario'),
	path('Producto/ContenidoLiterario/<int:primaryKey>', views.mostrarObraLiteraria)
# Create your views here.
		]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)