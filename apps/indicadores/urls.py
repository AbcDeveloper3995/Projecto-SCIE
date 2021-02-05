from django.urls import path
from apps.indicadores.views import *

app_name = 'indicador'

urlpatterns = [
    path('listarClasificador/', listarClasificadIndicadorView.as_view(), name='istarClasificador'),
    path('crearClasificador/', crearClasificadorIndicadorView.as_view(), name='crearClasificador'),
    path('modificarClasificador/<int:pk>/', updateClasificadorIndView.as_view(), name='updateClasificador'),
    path('eliminarClasificadorInd/<int:pk>/', eliminarClasificadorInd.as_view(), name='eliminarClasificadorInd'),
    path('listarIndicador/', listarIndicadorView.as_view(), name='listarIndicador'),
    path('crearIndicador/', crearIndicadorView.as_view(), name='crearIndicador'),
    path('modificarIndicador/<int:pk>/', updateIndicadorView.as_view(), name='updateIndicador'),
    path('eliminarIndicador/<int:pk>/', eliminarIndicador.as_view(), name='eliminarIndicador'),
    path('listarRespuesta/', listarPosiblesRespuestasView.as_view(), name='listarRespuesta'),
    path('crearRespuesta/', crearPosiblesRespuestasView.as_view(), name='crearRespuesta'),
    path('modificarRespuestas/<int:pk>/', updatePosiblresResView.as_view(), name='updateRespuestas'),
    path('eliminarRespuesta/<int:pk>/', eliminarPosibleRes.as_view(), name='eliminarRespuesta'),

]