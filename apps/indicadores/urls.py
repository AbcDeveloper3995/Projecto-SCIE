from django.urls import path
from apps.indicadores.views import *

app_name = 'indicador'

urlpatterns = [
    # LISTAR
    path('listarClasificador/', listarClasificadIndicadorView.as_view(), name='istarClasificador'),
    path('listarIndicador/', listarIndicadorView.as_view(), name='listarIndicador'),
    path('listarRespuesta/', listarPosiblesRespuestasView.as_view(), name='listarRespuesta'),

    # CREAR
    path('crearClasificador/', crearClasificadorIndicadorView.as_view(), name='crearClasificador'),
    path('crearIndicador/', crearIndicadorView.as_view(), name='crearIndicador'),
    path('crearRespuesta/', crearPosiblesRespuestasView.as_view(), name='crearRespuesta'),

    # MODIFICAR
    path('modificarClasificador/<int:pk>/', updateClasificadorIndView.as_view(), name='updateClasificador'),
    path('modificarIndicador/<int:pk>/', updateIndicadorView.as_view(), name='updateIndicador'),
    path('modificarRespuestas/<int:pk>/', updatePosiblresResView.as_view(), name='updateRespuestas'),

    # ELIMINAR
    path('eliminarClasificadorInd/<int:pk>/', eliminarClasificadorInd.as_view(), name='eliminarClasificadorInd'),
    path('eliminarIndicador/<int:pk>/', eliminarIndicador.as_view(), name='eliminarIndicador'),
    path('eliminarRespuesta/<int:pk>/', eliminarPosibleRes.as_view(), name='eliminarRespuesta'),












]