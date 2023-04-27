from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.

class Login(TemplateView):
    template_name = 'login.html'

class PaginaUsuario(TemplateView):
    template_name = 'usuario.html'

class AlteracaoSenha(TemplateView):
    template_name = 'alterar_senha.html'