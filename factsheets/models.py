from django.db import models
import os

def get_upload_path(instance, filename):
    return os.path.join('static/factsheets', instance.post.familia, filename)

# Define InformacaoFamilias
class InformacaoFamilias(models.Model):
    ano = models.IntegerField(help_text="Selecione o ano")
    autor = models.CharField(max_length=50)
    caracteristicas_gerais = models.TextField(verbose_name="Características Gerais",default="")
    diagnoses = models.TextField(verbose_name="Diagnoses")
    dados_geneticos = models.URLField(max_length=200,verbose_name="Dados genéticos",blank=True,null=True)
    familia = models.CharField(max_length=50,verbose_name='Família',unique=True)
    referencias = models.TextField(verbose_name="Referências",default="")

    def __str__(self):
        return f"{self.familia}"

# Define Imagens class usando InformacaoFamilias foreign key
class Imagens(models.Model):
    post = models.ForeignKey(InformacaoFamilias, on_delete=models.CASCADE, related_name='imagens',default='')
    # Este campo é para acessar a família
    familia = models.CharField(max_length=50,verbose_name='Família',unique=True,null=True)
    imagens = models.ImageField('Imagem',blank=True,upload_to=get_upload_path)
    legenda = models.TextField(verbose_name="Legenda",default="",blank=True)