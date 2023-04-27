from django.contrib import admin


from factsheets.models import InformacaoFamilias,Imagens

# Register your models here.

class MultipleImage(admin.ModelAdmin):
    class ImageInline(admin.TabularInline):
        model = Imagens
    inlines = [
        ImageInline,
    ]

admin.site.register(InformacaoFamilias,MultipleImage)