from django.contrib import admin
from homePage.models import Aficion 
from homePage.models import infousuario
from homePage.models import FormatoLiterario
from homePage.models import GeneroLiterario
from homePage.models import infoLibro
# Register your models here.
admin.site.register(Aficion)
admin.site.register(infousuario)
admin.site.register(FormatoLiterario)
admin.site.register(GeneroLiterario)
admin.site.register(infoLibro)