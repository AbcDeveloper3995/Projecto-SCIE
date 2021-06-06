from django.urls import path
from apps.guiaEstadistica.views import *

app_name = 'guia'

urlpatterns = [
    # LISTAR.
    path('listarGuias/', listarGuiasView.as_view(), name='listarGuias'),
    path('listarUniverso/', listarUniversoView.as_view(), name='listarUniverso'),

    # CREAR.
    path('crearGuias/', crearGuiasView.as_view(), name='crearGuias'),
    path('crearUniverso/', crearUniversoView.as_view(), name='crearUniverso'),

    # MODIFICAR.
    path('modificarGuias/<int:pk>/', updateGuiaView.as_view(), name='updateGuias'),
    path('modificarUniverso/<int:pk>/', updateUniversoView.as_view(), name='modificarUniverso'),

    # ELIMINAR.
    path('eliminarGuias/<int:pk>/', eliminarGuia.as_view(), name='eliminarGuias'),
    path('eliminarGuiaCaptada/<int:pk>/', eliminarGuiaCaptada.as_view(), name='eliminarGuiasCaptada'),
    path('eliminarUniverso/<int:pk>/', eliminarUniverso.as_view(), name='eliminarUniverso'),

    # PETICIONES AJAX.
    path('captarDatos/', captarDatosView.as_view(), name='captarDatos'),
    path('dataCaptacion/', dataCaptacion.as_view(), name='dataCaptacion'),
    path('guiaCaptada/', guiaCaptada.as_view(), name='guiaCaptada'),
    path('informacionCaptada/', informacionCaptada.as_view(), name='informacionCaptada'),
    path('seccionCaptada/', seccionCaptada.as_view(), name='seccionCaptada'),
    path('universo/', dataUniversoView.as_view(), name='dataUniverso'),
    path('modificarPreguntas/', modificarPreguntasView.as_view(), name='modificarPreguntas'),
    path('crearGuiaDefinida/', crearGuiaDefinida.as_view(), name='crearGuiaDefinidal'),

    # REPORTES.
    path('reporteGeneral/', reporteGeneralExcel.as_view(), name='reporteGeneral'),
    path('reporteVerificacion/', reporteVerificacionIndicadores.as_view(), name='reporteVerificacion'),
    path('reporteDisciplinaInfo/', reporteDisciplinaInformativa.as_view(), name='reporteDisciplinaInfo'),
    path('reporteErrores/', reporteSeñalamientosErrores.as_view(), name='reporteErrores'),
    path('reporteDomicilio/', reporteDomicilioSocial.as_view(), name='reporteDomicilio'),
    path('reporteUniverso/', reporteUniversoGuia.as_view(), name='reporteUniverso'),
    path('reporteCaptacion/', reporteCaptacion.as_view(), name='reporteCaptacion'),
 ]