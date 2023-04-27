from django.urls import path,re_path

# Importar classes do pacote views
from .views import FactSheets,FactSheetsFamilia,FactsheetsCreate,FactsheetsUpdate

urlpatterns = [
    #path('endereço/', PacoteView.as_view(),name='nome_da_url'),
    path('factsheets/',FactSheets.as_view(),name='factsheets'),
    re_path(r'factsheets/(?P<family>\w+)/$',FactSheetsFamilia.as_view(),name='factsheetsfamilia'),
    path('editar/factsheets/<int:pk>/',FactsheetsUpdate.as_view(),name='editar_factsheet'),
    path('cadastrar/factsheets/',FactsheetsCreate.as_view(),name='adicionarfactsheet'),
]