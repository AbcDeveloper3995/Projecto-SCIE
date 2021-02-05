from django.urls import path

from apps.entidad.views import *

app_name = 'entidad'

urlpatterns = [
    path('listarEntidad/', listarEntidadView.as_view(), name='listarEntidad'),
    path('crearEntidad/', crearEntidadView.as_view(), name='crearEntidad'),
    path('modificarEntidad/<int:pk>/', updateEntidadView.as_view(), name='modificarEntidad'),
    path('eliminarEntidad/<int:pk>/', eliminarEntidad.as_view(), name='eliminarEntidad'),

]