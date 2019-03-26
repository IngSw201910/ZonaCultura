from django.conf.urls import url
from . import views

urlpatterns=[
	url(r'^$', views.index, name='Home Page'),
	url(r'^Registro$', views.registro_view, name='JaveCultura Registro Page')
]
# Create your views here.
