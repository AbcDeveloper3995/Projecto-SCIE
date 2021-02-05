from django.contrib import admin
from apps.seccion.models import *


class seccionAdmin( admin.ModelAdmin):
    search_fields = ['nombre','guia_id']
    list_display = ('id', 'nombre','guia_id')
    list_filter = ('nombre', 'guia_id')


admin.site.register(seccion, seccionAdmin)
admin.site.register(clasificadorPeriodo)
admin.site.register(instanciaSeccion)
admin.site.register(nomencladorCodigo)
admin.site.register(nomencladorColumna)
admin.site.register(verificacion)
