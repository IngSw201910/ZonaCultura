from django.conf.urls import url
from . import views

urlpatterns=[
	url(r'^$', views.index, name='JaveCultura Home Page')
]
# Create your views here.
