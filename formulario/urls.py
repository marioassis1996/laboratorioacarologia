from django.urls import path

# importar as classes no pacote views
from .views import ColecaoCreate,ColecaoCSVCreate,ColecaoUpdate,ColecaoList,TomboList,Download,ColecaoAvancadoCreate

urlpatterns = [
    #path('endereço/', PacoteView.as_view(),name='nome_da_url'),
    path('cadastrar/colecao/',ColecaoCreate.as_view(),name='cadastrar_colecao'),
    path('cadastrar/csv/colecao/',ColecaoCSVCreate.as_view(),name='cadastrar_csv_colecao'),
    path('cadastrar/avancado/colecao/',ColecaoAvancadoCreate.as_view(),name='cadastrar_avancado_colecao'),
    path('editar/colecao/<int:pk>/',ColecaoUpdate.as_view(),name='editar_colecao'),
    path('listar/colecao/',ColecaoList.as_view(),name='listar_colecao'),
    path('confirma/tombo/',TomboList.as_view(),name='confirma_tombo'),
    path('download/',Download.colecao_csv,name='baixa'),
]