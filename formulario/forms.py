from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django_countries.widgets import CountrySelectWidget

from .models import Colecao

class ColecaoForm(ModelForm):
    # dateIdentified = forms.MultiValueField(fields=[forms.DateInput,forms.DateInput])
    # dateIdentified.render('data',['',''])
    class Meta:
        model = Colecao
        fields = ['catalogNumber','otherCatalogNumbers','recordedBy',
            'recordNumber','individualCount','sex','lifeStage','reproductiveCondition','preparations',
            'associatedTaxa','associatedReferences','associatedMedia','associatedSequences','occurrenceRemarks','eventDate',
            'eventTime','habitat','samplingProtocol','samplingEffort','eventRemarks','continent','country','countryCode',
            'stateProvince','county','municipality','island','islandGroup','waterBody','locality','locationRemarks',
            'minimumElevationInMeters','maximumElevationInMeters','minimumDepthInMeters','maximumDepthInMeters',
            'verbatimLatitude','verbatimLongitude','graus','minutos','segundos','Sul_Norte','graus_1','minutos_1','segundos_1',
            'w_O','decimalLatitude','decimalLongitude','coordinateUncertaintyInMeters',
            'geodeticDatum','georeferenceProtocol','georeferenceBy','georeferenceDate','georeferenceRemarks','kingdom',
            'phylum','classe','order','family','subfamily','genus','subgenus','specificEpithet','infraspecificEpithet',
            'scientificName','scientificNameAuthorShip','taxonRank','vernacularName','taxonRemarks','identificationQualifier',
            'typeStatus','identifiedBy','dateIdentified','identificationRemarks']
        if Colecao.objects.last():
            widgets = {
            'eventDate': forms.DateInput(attrs={'type': 'date','title':'asdf'}),
            'georeferenceDate': forms.DateInput(attrs={'type': 'date'}),
            'dateIdentified': forms.DateInput(attrs={'type': 'date'}),
            'eventTime': forms.TimeInput(attrs={'type': 'time'}),
            # 'country': CountrySelectWidget(),
            'catalogNumber': forms.TextInput(attrs={
                'placeholder': int(str(Colecao.objects.last()))+1,'class': 'col-lg-6 col-form-control',
                }),
        }

class ColecaoEditaForm(ModelForm):
    class Meta:
        model=Colecao
        fields = '__all__'
        if Colecao.objects.last():
            widgets = {
            'eventDate': forms.DateInput(attrs={'type': 'date'}),
            'georeferenceDate': forms.DateInput(attrs={'type': 'date'}),
            'dateIdentified': forms.DateInput(attrs={'type': 'date'}),
            'eventTime': forms.TimeInput(attrs={'type': 'time'}),
            'catalogNumber': forms.TextInput(attrs={
                'placeholder': int(str(Colecao.objects.last()))+1,'class': 'col-lg-6 col-form-control',
                }),
        }

class CsvForm(ModelForm):
    file = forms.FileField(label='arquivo')
    file.widget.attrs.update({'class':''})
    class Meta:
        model = Colecao
        fields = ['file']