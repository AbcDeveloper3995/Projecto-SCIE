from django.urls import path
from apps.guiaEstadistica.views import *

app_name = 'guia'

urlpatterns = [
    path('listarGuias/', listarGuiasView.as_view(), name='listarGuias'),
    path('crearGuias/', crearGuiasView.as_view(), name='crearGuias'),
    path('modificarGuias/<int:pk>/', updateGuiaView.as_view(), name='updateGuias'),
    path('eliminarGuias/<int:pk>/', eliminarGuia.as_view(), name='eliminarGuias'),
    path('captarDatos/', captarDatosView.as_view(), name='captarDatos'),
    path('dataCaptacion/', dataCaptacion.as_view(), name='dataCaptacion'),
    path('guiaCaptada/', guiaCaptada.as_view(), name='guiaCaptada'),
    path('eliminarGuiaCaptada/<int:pk>/', eliminarGuiaCaptada.as_view(), name='eliminarGuiasCaptada'),
    path('informacionCaptada/', informacionCaptada.as_view(), name='informacionCaptada'),
    path('seccionCaptada/', seccionCaptada.as_view(), name='seccionCaptada'),
    path('modificarUniverso/<int:pk>/', updateUniversoView.as_view(), name='modificarUniverso'),
    path('universo/', dataUniversoView.as_view(), name='dataUniverso'),
    path('crearUniverso/', crearUniversoView.as_view(), name='crearUniverso'),
    path('listarUniverso/', listarUniversoView.as_view(), name='listarUniverso'),
    path('eliminarUniverso/<int:pk>/', eliminarUniverso.as_view(), name='eliminarUniverso'),
    path('modificarPreguntas/', modificarPreguntasView.as_view(), name='modificarPreguntas'),

]