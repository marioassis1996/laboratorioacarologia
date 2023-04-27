from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import Max,Min
from django.utils.safestring import mark_safe
from django.views.generic.edit import CreateView,UpdateView
from formulario.models import Colecao
from factsheets.models import Imagens,InformacaoFamilias
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from folium import Marker,Map

from .forms import FactsheetsForm,FactsheetsUpdateForm

# Create your views here.

class FactSheets(TemplateView):
    template_name = 'factsheets.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['familia'] = Colecao.objects.values('family').distinct().order_by('family').exclude(family='')
        return context

class FactSheetsFamilia(TemplateView):
    template_name = 'factsheets_familia.html'
    # Função que gera o mapa
    def fazer_mapa(self):
        family = self.kwargs['family']
        
        # zoom do mapa
        zoom = 4

        # chamar apenas os objetos de determinada família
        colecaos = Colecao.objects.filter(family=family)

        # Lista com o maior e menor valor de latitude e longitude
        latitude = list(Colecao.objects.filter(family=family).aggregate(Max('decimalLatitude'),Min('decimalLatitude')).values())
        longitude = list(Colecao.objects.filter(family=family).aggregate(Max('decimalLongitude'),Min('decimalLongitude')).values())

        if latitude == [None,None] and longitude == [None,None]:
            latitude = [-19.8688655,-19.8688655]
            longitude = [-43.9695513,-43.9695513]
            zoom = 16

        # média de onde será o meio do mapa
        latitudemedia = (sum(latitude))/2
        longitudemedia = (sum(longitude))/2
        
        mapa_familia = Map(location=[latitudemedia,longitudemedia],zoom_start=zoom,tiles='Stamen Terrain')
        for colecao in colecaos:
            if colecao.decimalLatitude and colecao.decimalLongitude:
                lat = colecao.decimalLatitude
                lon = colecao.decimalLongitude
                Marker([lat, lon],popup = colecao.language).add_to(mapa_familia)
        return mapa_familia._repr_html_()
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        # Gera somente a div do mapa
        context['map'] = mark_safe(self.fazer_mapa())
        return render(request,self.template_name,context)

    def get_context_data(self, **kwargs):
        family = self.kwargs['family']
        context = super().get_context_data(**kwargs)
        generoscolecao = Colecao.objects.filter(family=family).order_by("genus")
        context['genero'] = generoscolecao.values('genus').distinct()
        context['especie'] = generoscolecao.order_by("scientificName").values('scientificName').distinct()
        context['familia'] = InformacaoFamilias.objects.filter(familia=family)
        context['imagem'] = Imagens.objects.filter(familia=family)
        return context

# Adicionar novo factsheets

class FactsheetsCreate(LoginRequiredMixin,CreateView,):
    form_class = FactsheetsForm
    login_url = reverse_lazy('login')
    model = InformacaoFamilias
    template_name = 'add_factsheets.html'
    success_url = reverse_lazy('factsheets')
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            familia = form.save()
            for i in range(1, 61):
                image = request.FILES.get(f'image{i}')
                legend = request.POST.get(f'legend{i}')
                if image:
                    familia.imagens.create(image=image, legenda=legend)
            return self.form_valid(form)
        else:
            self.object = None
            return self.form_invalid(form)

# UPDATE factsheets

class FactsheetsUpdate(LoginRequiredMixin,UpdateView):
    form_class = FactsheetsUpdateForm
    template_name = 'add_factsheets.html'
    model = InformacaoFamilias
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('factsheets')