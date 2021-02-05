from django.urls import path

from apps.seccion.views import *

app_name = 'seccion'

urlpatterns = [
    path('listarSeccion/', listarSeccionView.as_view(), name='listarSeccion'),
    path('crearSeccion/', crearSeccionView.as_view(), name='crearSeccion'),
    path('modificarSeccion/<int:pk>/', updateSeccionView.as_view(), name='updateSeccion'),
    path('eliminarSeccion/<int:pk>/', eliminarSeccion.as_view(), name='eliminarSeccion'),
    path('listarPeriodo/', listarPeriodoView.as_view(), name='listarPeriodo'),
    path('crearPeriodo/', crearPeriodoView.as_view(), name='crearPeriodo'),
    path('modificarPeriodo/<int:pk>/', updatePeriodoView.as_view(), name='updatePeriodo'),
    path('eliminarPeriodo/<int:pk>/', eliminarPeriodo.as_view(), name='eliminarPeriodo'),
    path('listarCodigo/', listarCodigoView.as_view(), name='listarCodigo'),
    path('crearCodigo/', crearCodigoView.as_view(), name='crearCodigo'),
    path('modificarCodigo/<int:pk>/', updateCodigoView.as_view(), name='updateCodigo'),
    path('eliminarCodigo/<int:pk>/', eliminarCodigo.as_view(), name='eliminarCodigo'),
    path('listarColumna/', listarColumnaView.as_view(), name='listarColumna'),
    path('crearColumna/', crearColumnaView.as_view(), name='crearColumna'),
    path('modificarColumna/<int:pk>/', updateColumnaView.as_view(), name='updateColumna'),
    path('eliminarColumna/<int:pk>/', eliminarColumna.as_view(), name='eliminarColumna'),
    path('crearInstancia/', crearInstanciaView.as_view(), name='crearInstancia'),
    path('getColumnas/', getColumnas.as_view(), name='getColumnas'),
    path('getCodigos/', getCodigos.as_view(), name='getCodigos'),
    path('comprobacionInd/<int:pk>/', comprobarIndicadoresEvaluados.as_view(), name='comprobacionInd'),
    path('modificarInstancias/', modificarInstanciasView.as_view(), name='modificarInstancias'),
]