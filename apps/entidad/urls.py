from django.urls import path

from apps.entidad.views import *

app_name = 'entidad'

urlpatterns = [
    path('listarEntidad/', listarEntidadView.as_view(), name='listarEntidad'),
    path('crearEntidad/', crearEntidadView.as_view(), name='crearEntidad'),
    path('modificarEntidad/<int:pk>/', updateEntidadView.as_view(), name='modificarEntidad'),
    path('eliminarEntidad/<int:pk>/', eliminarEntidad.as_view(), name='eliminarEntidad'),
    path('eliminarCIselected/', eliminarCIselectedView.as_view(), name='eliminarCIselected'),

    #IMPORTACIONES
    path('importarEntidad/', importarEntidad.as_view(), name='importarEntidad'),
    path('importarNAE/', importarNAE.as_view(), name='importarNAE'),
    path('importarOSDE/', importarOSDE.as_view(), name='importarOSDE'),
    path('importarORG/', importarOrganismo.as_view(), name='importarORG'),
    path('importarDPA/', importarDPA.as_view(), name='importarDPA'),

]