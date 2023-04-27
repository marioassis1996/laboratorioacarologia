from django.urls import path
from django.contrib.auth import views as auth_views

# Importar classes do pacote views
from .views import AlteracaoSenha,PaginaUsuario

urlpatterns = [
    #path('endereço/', PacoteView.as_view(),name='nome_da_url'),
    path('login/',auth_views.LoginView.as_view(template_name='login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='logout.html'),name='logout'),
    path('usuario/',PaginaUsuario.as_view(),name='paginausuario'),
    path('alterar/senha/', AlteracaoSenha.as_view(),name='alterarsenha'),
]