from django.urls import path

from apps.seccion.views import *

app_name = 'seccion'

urlpatterns = [
    # LISTAR
    path('listarSeccion/', listarSeccionView.as_view(), name='listarSeccion'),
    path('listarPeriodo/', listarPeriodoView.as_view(), name='listarPeriodo'),
    path('listarCodigo/', listarCodigoView.as_view(), name='listarCodigo'),
    path('listarColumna/', listarColumnaView.as_view(), name='listarColumna'),

    # CREAR
    path('crearSeccion/', crearSeccionView.as_view(), name='crearSeccion'),
    path('crearPeriodo/', crearPeriodoView.as_view(), name='crearPeriodo'),
    path('crearCodigo/', crearCodigoView.as_view(), name='crearCodigo'),
    path('crearColumna/', crearColumnaView.as_view(), name='crearColumna'),

    # MODIFICAR
    path('modificarSeccion/<int:pk>/', updateSeccionView.as_view(), name='updateSeccion'),
    path('modificarPeriodo/<int:pk>/', updatePeriodoView.as_view(), name='updatePeriodo'),
    path('modificarCodigo/<int:pk>/', updateCodigoView.as_view(), name='updateCodigo'),
    path('modificarColumna/<int:pk>/', updateColumnaView.as_view(), name='updateColumna'),
    path('editarInstancia/<int:pk>/', updateInstanciaView.as_view(), name='updateColumna'),

    # ELIMINAR
    path('eliminarSeccion/<int:pk>/', eliminarSeccion.as_view(), name='eliminarSeccion'),
    path('eliminarPeriodo/<int:pk>/', eliminarPeriodo.as_view(), name='eliminarPeriodo'),
    path('eliminarCodigo/<int:pk>/', eliminarCodigo.as_view(), name='eliminarCodigo'),
    path('eliminarColumna/<int:pk>/', eliminarColumna.as_view(), name='eliminarColumna'),
    path('eliminarInstancia/<int:pk>/', eliminarInstanciaView.as_view(), name='eliminarColumna'),

    # PETICIONES AJAX
    path('crearInstancia/', crearInstanciaView.as_view(), name='crearInstancia'),
    path('getColumnas/', getColumnas.as_view(), name='getColumnas'),
    path('getCodigos/', getCodigos.as_view(), name='getCodigos'),
    path('comprobacionInd/<int:pk>/', comprobarIndicadoresEvaluados.as_view(), name='comprobacionInd'),
    path('modificarInstancias/', modificarInstanciasView.as_view(), name='modificarInstancias'),
    path('valorIndVerificado/', valorIndicadoresVerificados.as_view(), name='valorIndVerificado'),
    path('indicadoresCoinciden/', indicadoresCoinciden.as_view(), name='indicadoresCoinciden'),

















]