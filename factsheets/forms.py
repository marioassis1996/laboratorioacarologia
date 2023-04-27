from django import forms
from django.utils import timezone
from factsheets.models import InformacaoFamilias
from formulario.models import Colecao

def get_ano_choice():
    return [(r,r) for r in range(1950,timezone.now().year+1)]

def get_choices_list():
    excluir = ['']
    for i in list(Colecao.objects.order_by('family').values_list('family',flat=True).distinct()):
        if i in list(InformacaoFamilias.objects.values_list('familia',flat=True)):
            excluir.append(i)

    families = Colecao.objects.order_by('family').values_list('family',flat=True).distinct().exclude(family__in=excluir)
    return [(r,r) for r in families]

def get_ano_choice():
    return [(r,r) for r in range(timezone.now().year,1950,-1)]

class FactsheetsForm(forms.ModelForm):
    ano = forms.ChoiceField(choices=get_ano_choice)
    autor = forms.CharField(max_length=50)
    caracteristicas_gerais = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    dados_geneticos = forms.URLField(max_length=200)
    diagnoses = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    familia = forms.ChoiceField(label='Família',choices=get_choices_list)
    referencias = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))

    class Meta:
        model = InformacaoFamilias
        fields = ['familia','autor','ano','dados_geneticos','diagnoses','caracteristicas_gerais','referencias']
        widget={
            'ano':'',
            'autor':'',
            'caracteristicas_gerais':'',
            'dados_geneticos':'',
            'diagnoses':'',
            'familia':'',
            'imagens':'',
            'legenda':'',
            'referencias':'',
        }

    def save(self, commit=True):
        familia = super().save(commit=False)
        if commit:
            familia.save()

        imagens = self.cleaned_data.get('imagens')
        legendas = self.cleaned_data.get('legendas').splitlines() if self.cleaned_data.get('legendas') else []
        if imagens:
            for i, imagem in enumerate(imagens):
                legenda = legendas[i] if i < len(legendas) else ''
                familia.imagens.create(image=imagem, legenda=legenda)
        return familia

class FactsheetsUpdateForm(forms.ModelForm):
    class Meta:
        model = InformacaoFamilias
        fields = ['familia','autor','ano','dados_geneticos','diagnoses','caracteristicas_gerais','referencias']
        widget={
            'ano':'',
            'autor':'',
            'caracteristicas_gerais':'',
            'dados_geneticos':'',
            'diagnoses':'',
            'familia':'',
            'imagens':'',
            'legenda':'',
            'referencias':'',
        }