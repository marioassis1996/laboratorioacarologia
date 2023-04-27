from django.db import models
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Colecao(models.Model):
    # choices do formulário
    BASISOFRECORDCHOICES = [("PreservedSpecimen","PreservedSpecimen"),("FossilSpecimen","FossilSpecimen"),
                            ("LivingSpecimen","LivingSpecimen"),("MaterialSample","MaterialSample"),("Event","Event"),
                            ("HumanObservation","HumanObservation"),("MachineObservation","MachineObservation"),
                            ("Taxon","Taxon"),("Occurrence","Occurrence"),("MaterialCitation","MaterialCitation")]
    LICENSECHOICES = [("CC","CC"),("CC BY","CC BY"),("CC BY NC","CC BY NC")]
    SEXCHOICES = [("Selecione","Selecione"),("Fêmea","Fêmea"),("Macho","Macho"),("Hermafrodita","Hermafrodita"),
                  ("Não se aplica","Não se aplica")]
    LIFESTAGECHOICES = [("Selecione","Selecione"),("Ovo","Ovo"),("Adulto","Adulto"),("Protonifa","Protoninfa"),
                        ("Deutoninfa","Deutoninfa"),("Larva","Larva"),("Tritoninfa","Tritoninfa")]
    CONTINENTCHOICES = [("América do Sul","América do Sul"),("África","África"),("América Central","América Central"),
                        ("América do Norte","América do Norte"),("Antártica","Antártica"),("Ártico","Ártico"),("Ásia","Ásia"),
                        ("Europa","Europa"),("Oceania","Oceania")]
    TAXONRANKSCHOICES = [("Espécie","Espécie"),("Subgênero","Subgênero"),("Genero","Gênero"),("Subfamília","Subfamília"),
                        ("Familia","Família"),("Ordem","Ordem"),("Classe","Classe"),("Filo","Filo"),("Reino","Reino")]
    SULNORTECHOICES = [(-1,'S'),(1,'N')]
    LESTEOESTECHOICES = [(-1,'L'),(1,'O')]

    # variáveis do models
    basisOfRecord = models.CharField(max_length=18,verbose_name="Natureza do Registro",choices=BASISOFRECORDCHOICES,default="PreservedSpecimen",help_text="")
    modified = models.DateField(auto_now=True)
    datasetName = models.CharField(max_length=107, verbose_name="Nome do conjunto de dados", default="Coleção de Acarologia, Centro de coleções taxonômicas (CCT), da Universidade Federal de Minas Gerais (UFMG)",help_text="")
    type = models.CharField(max_length=15, verbose_name="Tipo",default="Coleção",help_text="")
    language = models.CharField(max_length=5,default="pt",verbose_name="Idioma",help_text="")
    institutionID = models.CharField(max_length=50, default="",verbose_name="ID da instituição",blank=True,help_text="")
    institutionCode = models.CharField(max_length=10,default="UFMG-CCT",verbose_name="Código da instituição",help_text="")
    collectionCode = models.CharField(max_length=10,default="UFMG-AC",verbose_name="Código da coleção",help_text="")
    license = models.CharField(max_length=8,choices=LICENSECHOICES,default="NC",verbose_name="Licença",help_text="")
    rightsHolder = models.CharField(max_length=43,default="Universidade Federal de Minas Gerais (UFMG)",verbose_name="Titular dos direitos",help_text="")
    dynamicProperties = models.CharField(max_length=50,blank=True,verbose_name="Propriedades dinâmicas",help_text="")
    occurrenceID = models.CharField(max_length=50,default="Br:UFMG-CCT:UFMG-AC:",verbose_name="ID da ocorrência",help_text="")
    catalogNumber = models.CharField(max_length=50,unique=True,verbose_name="Tombo",help_text="")
    otherCatalogNumbers = models.CharField(max_length=20,blank=True,verbose_name="Outros números de Tombo",help_text="")
    recordedBy = models.CharField(max_length=70,blank=True,verbose_name="Registrado por",help_text="")
    recordNumber = models.CharField(max_length=50,blank=True,verbose_name="Número do registro",help_text="")
    individualCount = models.CharField(max_length=20,blank=True,verbose_name="Número de indvíduos",help_text="")
    sex = models.CharField(max_length=13,choices=SEXCHOICES,default="Selecione",blank=True,verbose_name="Sexo",help_text="")
    lifeStage = models.CharField(max_length=15,choices=LIFESTAGECHOICES,blank=True,verbose_name="Etapa de vida",help_text="")
    reproductiveCondition = models.CharField(max_length=15,blank=True,verbose_name="Condição reprodutiva",help_text="")
    preparations = models.CharField(max_length=15,blank=True,verbose_name="Preparações",help_text="")
    disposition = models.CharField(max_length=15,default="na coleção",blank=True,verbose_name="Disposição",help_text="")
    associatedTaxa = models.TextField(default="",blank=True,verbose_name="Táxons associados",help_text="")
    associatedReferences = models.TextField(blank=True,verbose_name="Referências associadas",help_text="")
    associatedMedia = models.URLField(max_length=200,blank=True,verbose_name="Mídia Associada",help_text="")
    associatedSequences = models.TextField(blank=True,verbose_name="Sequência Associada",help_text="")
    occurrenceRemarks = models.TextField(default="",blank=True,verbose_name="Comentários da ocorrência",help_text="")
    eventDate = models.CharField(max_length=50,null=True,blank=True,verbose_name="Data do evento",help_text="")
    eventTime = models.TimeField(null=True,blank=True,verbose_name="Hora do evento",help_text="",editable=True)
    habitat = models.TextField(default="",blank=True,verbose_name="Habitat",help_text="")
    samplingProtocol = models.CharField(max_length=50,blank=True,verbose_name="Protocolo da amostra",help_text="")
    samplingEffort = models.CharField(max_length=50,blank=True,verbose_name="Esforço da amostragem",help_text="")
    eventRemarks = models.TextField(default="",blank=True,verbose_name="Comentários do evento",help_text="")
    continent = models.CharField(max_length=22,choices=CONTINENTCHOICES,blank=True,verbose_name="Continente",help_text="")
    country = CountryField(blank=True, null=True)
    countryCode = models.CharField(max_length=3,blank=True,verbose_name="Código do país",help_text="")
    stateProvince = models.CharField(max_length=50,blank=True,verbose_name="Estado/Província",help_text="")
    county = models.CharField(max_length=50,blank=True,verbose_name="Município",help_text="")
    municipality = models.CharField(max_length=50,blank=True,verbose_name="Distrito",help_text="")
    island = models.CharField(max_length=50,blank=True,verbose_name="Ilha",help_text="")
    islandGroup = models.CharField(max_length=50,blank=True,verbose_name="Arquipélago",help_text="")
    waterBody = models.CharField(max_length=50,blank=True,verbose_name="Corpo d'água",help_text="")
    locality = models.CharField(max_length=100,blank=True,verbose_name="Localidade",help_text="")
    locationRemarks = models.TextField(default="",blank=True,verbose_name="Comentários da localização",help_text="")
    minimumElevationInMeters = models.IntegerField(null=True,blank=True,verbose_name="Elevação mínima em metros",help_text="")
    maximumElevationInMeters = models.IntegerField(null=True,blank=True,verbose_name="Elevação máxima em metros",help_text="")
    minimumDepthInMeters = models.IntegerField(null=True,blank=True,verbose_name="Profundidade mínima em metros",help_text="")
    maximumDepthInMeters = models.IntegerField(null=True,blank=True,verbose_name="Profundidade máxima em metros",help_text="")
    verbatimLatitude = models.CharField(max_length=50,blank=True,verbose_name="Latitude (XX S/N XX' XX\")",help_text="")
    verbatimLongitude = models.CharField(max_length=50,blank=True,verbose_name="Longitude (XX W/O XX' XX\")",help_text="")
    verbatimCoordinates = models.CharField(max_length=50,blank=True,verbose_name="Latitude e Longitude",help_text="")
    graus = models.PositiveSmallIntegerField(blank=True,null=True,verbose_name="Graus Latitude",help_text="")
    minutos = models.PositiveSmallIntegerField(blank=True,null=True,verbose_name="Minutos Latidude",help_text="")
    segundos = models.FloatField(blank=True, null=True,verbose_name="Segundos Latitude",help_text="")
    Sul_Norte = models.SmallIntegerField(blank=True,null=True,db_column="S/N",choices=SULNORTECHOICES,verbose_name="Sul/Norte",help_text="")
    graus_1 = models.PositiveSmallIntegerField(null=True,blank=True,db_column="graus.1",verbose_name="Graus Longitude",help_text="")
    minutos_1 = models.PositiveSmallIntegerField(null=True,blank=True,db_column="minutos.1",verbose_name="Minutos Longitude",help_text="")
    segundos_1 = models.FloatField(null=True,blank=True,db_column="segundos.1",verbose_name="Segundos Longitude",help_text="")
    w_O = models.SmallIntegerField(null=True,blank=True,choices=LESTEOESTECHOICES,db_column="W/O",verbose_name="Leste/Oeste",help_text="")
    decimalLatitude = models.FloatField(verbose_name="Latitude em decimal",help_text="",null=True,blank=True)
    decimalLongitude = models.FloatField(verbose_name="Longitude em decimal",help_text="",null=True,blank=True)
    coordinateUncertaintyInMeters = models.CharField(max_length=50,blank=True,verbose_name="Incerteza na coordenada em metros",help_text="")
    geodeticDatum = models.CharField(max_length=80,blank=True,verbose_name="Dado geodésico",help_text="")
    georeferenceProtocol = models.TextField(default="",blank=True,verbose_name="Protocolo de georreferenciamento",help_text="")
    georeferenceBy = models.CharField(max_length=200,blank=True,verbose_name="Georreferenciado por",help_text="")
    georeferenceDate = models.CharField(max_length=50,verbose_name="Data do georeferenciamento",help_text="",blank=True, null=True)
    georeferenceRemarks = models.TextField(blank=True,verbose_name="Comentários do georreferenciamento",help_text="")
    kingdom = models.CharField(max_length=50,default="Animalia",blank=True,verbose_name="Reino",help_text="")
    phylum = models.CharField(max_length=50,default="Arthropoda",blank=True,verbose_name="Filo",help_text="")
    classe = models.CharField(max_length=50,default="Acari",blank=True,db_column="class",verbose_name="Classe",help_text="")
    order = models.CharField(max_length=50,blank=True,verbose_name="Ordem",help_text="")
    family = models.CharField(max_length=50,blank=True,verbose_name="Família",help_text="")
    subfamily = models.CharField(max_length=50,blank=True,verbose_name="Sub-família",help_text="")
    genus = models.CharField(max_length=50,blank=True,verbose_name="Gênero",help_text="")
    subgenus = models.CharField(max_length=50,blank=True,verbose_name="Sub-gênero",help_text="")
    specificEpithet = models.CharField(max_length=50,blank=True,verbose_name="Epíteto específico",help_text="")
    infraspecificEpithet = models.CharField(max_length=50,blank=True,verbose_name="Epíteto infraespecífico",help_text="")
    scientificName = models.CharField(max_length=50,blank=True,verbose_name="Nome científico",help_text="")
    scientificNameAuthorShip = models.CharField(max_length=100,blank=True,verbose_name="Autoria do nome científico",help_text="")
    taxonRank = models.CharField(max_length=50,choices=TAXONRANKSCHOICES,blank=True,verbose_name="Nível científico",help_text="")
    vernacularName = models.CharField(max_length=50,blank=True,verbose_name="Nome comum",help_text="")
    taxonRemarks = models.TextField(default="",blank=True,verbose_name="Comentário sobre o táxon",help_text="")
    identificationQualifier = models.CharField(max_length=50,blank=True,verbose_name="Qualificador da identificação",help_text="")
    typeStatus = models.CharField(max_length=50,blank=True,verbose_name="Condição do tipo",help_text="")
    identifiedBy = models.CharField(max_length=200,blank=True,verbose_name="Identificado por",help_text="")
    dateIdentified = models.CharField(max_length=50,null=True,blank=True,verbose_name="Data da identificação",help_text="")
    identificationRemarks = models.TextField(blank=True,verbose_name="Comentários da identificação",help_text="")

    def __str__(self):
        # Aparece no campo (mudar para o tombo e alguma outra informação)
        return f"{self.catalogNumber}"