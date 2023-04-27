import csv
import pandas as pd

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.views.generic.list import ListView
from django.contrib import messages
from django.shortcuts import redirect

#Importar as classes do models e forms
from .forms import ColecaoEditaForm, ColecaoForm, CsvForm
from .models import Colecao

# Create your views here.

# String aparece duas vezes
template_formulario ='formulario/formulario.html'

# Adicionar nova exemplar na coleção
# não precisa de login para visualizar, sem o login não aparece o botão de confirmar
class ColecaoCreate(CreateView):
    form_class = ColecaoForm
    template_name = template_formulario
    success_url = reverse_lazy('listar_colecao')

    def get_context_data(self,*args,**kwargs):
        
        context = super().get_context_data(*args,**kwargs)
        context['titulo'] = 'Formulário de novos tombamentos'
        context['naologado'] = 'É necessário fazer login para salvar o registro.'
        context['avancado'] = 'Formulário de cadastro avançado.'
        context['mensagem'] = 'Preencha os campos obrigatórios.'

        return context

    def form_valid(self,form):
        if (
            form.instance.decimalLatitude != pd.notnull and form.instance.graus and form.instance.minutos
            and form.instance.segundos and form.instance.Sul_Norte
        ):
            form.instance.decimalLatitude = (
                form.instance.graus + form.instance.minutos/60 + form.instance.segundos/3600
            )*form.instance.Sul_Norte
        if (
            form.instance.decimalLongitude != pd.notnull and form.instance.graus_1 and form.instance.minutos_1 
            and form.instance.segundos_1 and form.instance.w_O
        ):
            form.instance.decimalLongitude = (
                form.instance.graus_1 + form.instance.minutos_1/60 + form.instance.segundos_1/3600
            )*form.instance.w_O

        # Após esse comando os dados são salvos
        url = super().form_valid(form)

        # Trocando as informações das coordenadas
        if self.object.Sul_Norte == -1:
            sulnorte = 'S'
        elif self.object.Sul_Norte == 1:
            sulnorte = 'N'

        if self.object.w_O == -1:
            lesteoeste = 'W'
        elif self.object.w_O == 1:
            lesteoeste = 'E'

        if (
            self.object.graus and self.object.minutos and self.object.segundos and self.object.graus_1
            and self.object.minutos_1 and self.object.segundos_1 and self.object.Sul_Norte and self.object.w_O
        ):
            self.object.verbatimLatitude = str(
                str(self.object.graus) + sulnorte +''+ str(self.object.minutos) +'\''+ str(self.object.segundos)+'\"'
            )
            self.object.verbatimLongitude = str(
                str(self.object.graus_1) + lesteoeste +''+ str(self.object.minutos_1) +'\''+ str(self.object.segundos_1)+'\"'
            )
            self.object.verbatimCoordinates = self.object.verbatimLongitude + ',' + self.object.verbatimLatitude
        
        if self.object.country:
            self.object.countryCode = self.object.country.code
            self.object.country = self.object.country.name

        self.object.occurrenceID += self.object.catalogNumber
        self.object.save()

        return url

# Adicionar coleção avançado
class ColecaoAvancadoCreate(LoginRequiredMixin,CreateView):
    login_url = reverse_lazy('login')
    model = Colecao
    fields = '__all__'
    template_name = template_formulario
    success_url = reverse_lazy('listar_colecao')
    
    def get_context_data(self,*args,**kwargs):

        context = super().get_context_data(*args,**kwargs)
        context['titulo'] = 'Formulário de tombamento'
        context['naologado'] = 'É necessário fazer login para salvar o registro.'
        context['mensagem'] = 'Cadastro Avançado da Coleção'

        return context

    def form_valid(self,form):
        if (
            form.instance.decimalLatitude != pd.notnull and form.instance.graus and form.instance.minutos
            and form.instance.segundos and form.instance.Sul_Norte
        ):
            form.instance.decimalLatitude = (
                form.instance.graus + form.instance.minutos/60 + form.instance.segundos/3600
            )*form.instance.Sul_Norte
        if (
            form.instance.decimalLongitude != pd.notnull and form.instance.graus_1 and form.instance.minutos_1 
            and form.instance.segundos_1 and form.instance.w_O
        ):
            form.instance.decimalLongitude = (
                form.instance.graus_1 + form.instance.minutos_1/60 + form.instance.segundos_1/3600
            )*form.instance.w_O

        # Após esse comando os dados são salvos
        url = super().form_valid(form)

        # Trocando as informações sobre colocar as coordenadas
        if self.object.Sul_Norte == -1:
            sulnorte = 'S'
        elif self.object.Sul_Norte == 1:
            sulnorte = 'N'

        if self.object.w_O == -1:
            lesteoeste = 'W'
        elif self.object.w_O == 1:
            lesteoeste = 'E'

        if (
            self.object.graus and self.object.minutos and self.object.segundos and self.object.graus_1
            and self.object.minutos_1 and self.object.segundos_1 and self.object.Sul_Norte and self.object.w_O
        ):
            self.object.verbatimLatitude = str(
                str(self.object.graus) + sulnorte +''+ str(self.object.minutos) +'\''+ str(self.object.segundos)+'\"'
            )
            self.object.verbatimLongitude = str(
                str(self.object.graus_1) + lesteoeste +''+ str(self.object.minutos_1) +'\''+ str(self.object.segundos_1)+'\"'
            )
            self.object.verbatimCoordinates = self.object.verbatimLongitude + ',' + self.object.verbatimLatitude
        
        if self.object.country:
            self.object.countryCode = self.object.country.code
            self.object.country = self.object.country.name


        self.object.occurrenceID += self.object.catalogNumber
        self.object.save()

        return url

# Importar csv para banco de dados
class ColecaoCSVCreate(FormView):
    login_url = reverse_lazy('login')
    form_class = CsvForm
    template_name = 'formulario/formulario.html'
    success_url = reverse_lazy('listar_colecao')
    model = Colecao

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request,*args,**kwargs):
        files = request.FILES['file']
        df = pd.read_csv(files)
        
        correspondent_fields = {f.column:f for f in self.model._meta.get_fields()}
        dict_df = df.to_dict(orient='records')

        # Funçao que converte dados do formato do python para o formato do models
        def convert_values(k,v):
            if pd.isna(v):
                v = None
            # Muda os dados das colunas S/N e W/O para números
            if correspondent_fields[k].name == "Sul_Norte" and v:
                if v == "S":
                    v = -1
                else:
                    v = 1
            elif correspondent_fields[k].name == "w_O" and v:
                if v == "W":
                    v = -1
                else:
                    v = 1
            return correspondent_fields[k].to_python(v)

        for entry in dict_df:
            catalog_number = entry.get('catalogNumber')
            obj, created = self.model.objects.get_or_create(catalogNumber=catalog_number)
            if not created:
                messages.warning(self.request, f'Catalog Number {catalog_number} already exists.')

            else:
                obj.__dict__.update(**{correspondent_fields[k].name: convert_values(k,v) for k,v in entry.items() if convert_values(k,v)})
                obj.save()

        return redirect(self.success_url)

# UPDATE #
class ColecaoUpdate(LoginRequiredMixin,UpdateView):
    login_url = reverse_lazy('login')
    form_class = ColecaoEditaForm
    template_name = template_formulario
    success_url = reverse_lazy('listar_colecao')
    
    def form_valid(self,form):
        if (
            form.instance.decimalLatitude != pd.notnull and form.instance.graus and form.instance.minutos
            and form.instance.segundos and form.instance.Sul_Norte
        ):
            form.instance.decimalLatitude = (
                form.instance.graus + form.instance.minutos/60 + form.instance.segundos/3600
            )*form.instance.Sul_Norte
        if (
            form.instance.decimalLongitude != pd.notnull and form.instance.graus_1 and form.instance.minutos_1 
            and form.instance.segundos_1 and form.instance.w_O
        ):
            form.instance.decimalLongitude = (
                form.instance.graus_1 + form.instance.minutos_1/60 + form.instance.segundos_1/3600
            )*form.instance.w_O

        # Após esse comando os dados são salvos
        url = super().form_valid(form)

        # Trocando as informações sobre colocar as coordenadas
        if self.object.Sul_Norte == -1:
            sulnorte = 'S'
        elif self.object.Sul_Norte == 1:
            sulnorte = 'N'

        if self.object.w_O == -1:
            lesteoeste = 'W'
        elif self.object.w_O == 1:
            lesteoeste = 'E'

        if (
            self.object.graus and self.object.minutos and self.object.segundos and self.object.graus_1
            and self.object.minutos_1 and self.object.segundos_1 and self.object.Sul_Norte and self.object.w_O
        ):
            self.object.verbatimLatitude = str(
                str(self.object.graus) + sulnorte +''+ str(self.object.minutos) +'\''+ str(self.object.segundos)+'\"'
            )
            self.object.verbatimLongitude = str(
                str(self.object.graus_1) + lesteoeste +''+ str(self.object.minutos_1) +'\''+ str(self.object.segundos_1)+'\"'
            )
            self.object.verbatimCoordinates = self.object.verbatimLongitude + ',' + self.object.verbatimLatitude
        
        if self.object.country:
            self.object.countryCode = self.object.country.code
            self.object.country = self.object.country.name

        self.object.save()

        return url

# LIST #

form = ['catalogNumber','genus','family','occurrenceID']

class ColecaoList(ListView):
    model = Colecao
    '''form = ['basisOfRecord','datasetName','type','language','institutionID','institutionCode','collectionCode',
            'license','rightsHolder','dynamicProperties','occurrenceID','catalogNumber','otherCatalogNumbers','recordedBy',
            'recordNumber','individualCount','sex','lifeStage','reproductiveCondition','preparations','disposition',
            'associatedTaxa','associatedReferences','associatedMedia','associatedSequences','occurrenceRemarks','eventDate',
            'eventTime','habitat','samplingProtocol','samplingEffort','eventRemarks','continent','country','countryCode',
            'stateProvince','county','municipality','island','islandGroup','waterBody','locality','locationRemarks',
            'minimumElevationInMeters','maximumElevationInMeters','minimumDepthInMeters','maximumDepthInMeters',
            'verbatimLatitude','verbatimLongitude','decimalLatitude','decimalLongitude','coordinateUncertaintyInMeters',
            'geodeticDatum','georeferenceProtocol','georeferenceBy','georeferenceDate','georeferenceRemarks','kingdom',
            'phylum','classe','order','family','subfamily','genus','subgenus','specificEpithet','infraspecificEpithet',
            'scientificName','scientificNameAuthorShip','taxonRank','vernacularName','taxonRemarks','identificationQualifier',
            'typeStatus','identifiedBy','dateIdentified','identificationRemarks']'''
    form = form
    template_name = 'formulario/listar.html'
    paginate_by = 10
    def get_queryset(self):
        self.object_list = Colecao.objects.order_by("-catalogNumber")
        return self.object_list

class Download(TemplateView):
    def colecao_csv(self):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attchment; filename=UFMGAC.csv'

        writer = csv.writer(response)

        writer.writerow(['basisOfRecord','datasetName','type','language','institutionID','institutionCode','collectionCode',
            'license','rightsHolder','dynamicProperties','occurrenceID','catalogNumber','otherCatalogNumbers','recordedBy',
            'recordNumber','individualCount','sex','lifeStage','reproductiveCondition','preparations','disposition',
            'associatedTaxa','associatedReferences','associatedMedia','associatedSequences','occurrenceRemarks','eventDate',
            'eventTime','habitat','samplingProtocol','samplingEffort','eventRemarks','continent','country','countryCode',
            'stateProvince','county','municipality','island','islandGroup','waterBody','locality','locationRemarks',
            'minimumElevationInMeters','maximumElevationInMeters','minimumDepthInMeters','maximumDepthInMeters',
            'verbatimLatitude','verbatimLongitude','decimalLatitude','decimalLongitude','coordinateUncertaintyInMeters',
            'geodeticDatum','georeferenceProtocol','georeferenceBy','georeferenceDate','georeferenceRemarks','kingdom',
            'phylum','class','order','family','subfamily','genus','subgenus','specificEpithet','infraspecificEpithet',
            'scientificName','scientificNameAuthorShip','taxonRank','vernacularName','taxonRemarks','identificationQualifier',
            'typeStatus','identifiedBy','dateIdentified','identificationRemarks'])

        colecoes = Colecao.objects.all()

        for colecao in colecoes:
            writer.writerow([
                colecao.basisOfRecord,colecao.datasetName,colecao.type,colecao.language,colecao.institutionID,
                colecao.institutionCode,colecao.collectionCode,colecao.license,colecao.rightsHolder,colecao.dynamicProperties,
                colecao.occurrenceID,colecao.catalogNumber,colecao.otherCatalogNumbers,colecao.recordedBy,colecao.recordNumber,
                colecao.individualCount,colecao.sex,colecao.lifeStage,colecao.reproductiveCondition,colecao.preparations,
                colecao.disposition,colecao.associatedTaxa,colecao.associatedReferences,colecao.associatedMedia,
                colecao.associatedSequences,colecao.occurrenceRemarks,colecao.eventDate,colecao.eventTime,colecao.habitat,
                colecao.samplingProtocol,colecao.samplingEffort,colecao.eventRemarks,colecao.continent,colecao.country,
                colecao.countryCode,colecao.stateProvince,colecao.county,colecao.municipality,colecao.island,
                colecao.islandGroup,colecao.waterBody,colecao.locality,colecao.locationRemarks,colecao.minimumElevationInMeters,
                colecao.maximumElevationInMeters,colecao.minimumDepthInMeters,colecao.maximumDepthInMeters,
                colecao.verbatimLatitude,colecao.verbatimLongitude,colecao.decimalLatitude,colecao.decimalLongitude,
                colecao.coordinateUncertaintyInMeters,colecao.geodeticDatum,colecao.georeferenceProtocol,colecao.georeferenceBy,
                colecao.georeferenceDate,colecao.georeferenceRemarks,colecao.kingdom,colecao.phylum,colecao.classe,
                colecao.order,colecao.family,colecao.subfamily,colecao.genus,colecao.subgenus,colecao.specificEpithet,
                colecao.infraspecificEpithet,colecao.scientificName,colecao.scientificNameAuthorShip,colecao.taxonRank,
                colecao.vernacularName,colecao.taxonRemarks,colecao.identificationQualifier,colecao.typeStatus,
                colecao.identifiedBy,colecao.dateIdentified,colecao.identificationRemarks
            ])

        return response

class TomboList(ListView):
    model = Colecao
    template_name = 'formulario/confirma_formulario.html'
    def get_queryset(self):
        ultimoadicionado = Colecao.objects.last()
        self.object_list = Colecao.objects.filter(catalogNumber=ultimoadicionado)
        return self.object_list