from django.contrib import admin

#Importar as classes que apareceram no painel admin
from .models import Colecao

# Register your models here.
admin.site.register(Colecao)