from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from apps.entidad.models import *


class clasificador_DPA_Resource(resources.ModelResource):
    class Meta:
        model = clasificadorDPA

class clasificador_DPA_Admin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['codigo']
    list_display = ('codigo', 'descripcion')
    resource_class = clasificador_DPA_Resource

class clasificador_NAE_Resource(resources.ModelResource):
    class Meta:
        model = clasificadorNAE

class clasificador_NAE_Admin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['codigo']
    list_display = ('codigo','descripcion')
    resource_class = clasificador_NAE_Resource

class EntidadResource(resources.ModelResource):
    class Meta:
        model = Entidad

class EntidadAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['codigo_CI', 'nombre_CI']
    list_display = ('codigo_CI', 'nombre_CI', 'ote_codigo', 'ome_codigo', 'codigo_NAE', 'org_codigo', 'osde_codigo')
    resource_class = EntidadResource

class organismo_Resource(resources.ModelResource):
    class Meta:
        model = organismo

class organismo_Admin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['codigo']
    list_display = ('codigo', 'descripcion')
    resource_class = organismo_Resource

class osde_Resource(resources.ModelResource):
    class Meta:
        model = osde

class osde_Admin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['codigo']
    list_display = ('codigo', 'descripcion')
    resource_class = osde_Resource

class universoAdmin(admin.ModelAdmin):
    search_fields = ['guia']
    list_display = ('id', 'guia', 'entidad_codigo')
    list_filter = ('guia',)

admin.site.register(Entidad, EntidadAdmin)
admin.site.register(clasificadorDPA, clasificador_DPA_Admin)
admin.site.register(clasificadorNAE, clasificador_NAE_Admin)
admin.site.register(osde, osde_Admin)
admin.site.register(organismo, organismo_Admin)
