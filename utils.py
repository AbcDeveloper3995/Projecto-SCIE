from apps.guiaEstadistica.models import cuestionario
from apps.indicadores.models import Indicadores

# FUNCION PARA OBTENER UN LISTADO DE CUESTIONARIOS SEGUN EL PERMISO DEL USUARIO.
def getCuestionarios(user):
    if user.is_superuser:
        query = cuestionario.objects.all()
        return query
    elif user.has_perm('guiaEstadistica.pinar'):
        query = cuestionario.objects.filter(entidad_codigo__ote_codigo=21, guia__activo=True)
        return query
    elif user.has_perm('guiaEstadistica.artemisa'):
        query = cuestionario.objects.filter(entidad_codigo__ote_codigo=22, guia__activo=True)
        return query
    elif user.has_perm('guiaEstadistica.habana'):
        query = cuestionario.objects.filter(entidad_codigo__ote_codigo=23, guia__activo=True)
        return query
    elif user.has_perm('guiaEstadistica.mayabeque'):
        query = cuestionario.objects.filter(entidad_codigo__ote_codigo=24, guia__activo=True)
        return query
    elif user.has_perm('guiaEstadistica.matanzas'):
        query = cuestionario.objects.filter(entidad_codigo__ote_codigo=25, guia__activo=True)
        return query
    elif user.has_perm('guiaEstadistica.villa_clara'):
        query = cuestionario.objects.filter(entidad_codigo__ote_codigo=26, guia__activo=True)
        return query
    elif user.has_perm('guiaEstadistica.cienfuegos'):
        query = cuestionario.objects.filter(entidad_codigo__ote_codigo=27, guia__activo=True)
        return query
    elif user.has_perm('guiaEstadistica.santi_spiritu'):
        query = cuestionario.objects.filter(entidad_codigo__ote_codigo=28, guia__activo=True)
        return query
    elif user.has_perm('guiaEstadistica.ciego'):
        query = cuestionario.objects.filter(entidad_codigo__ote_codigo=29, guia__activo=True)
        return query
    elif user.has_perm('guiaEstadistica.camaguey'):
        query = cuestionario.objects.filter(entidad_codigo__ote_codigo=30, guia__activo=True)
        return query
    elif user.has_perm('guiaEstadistica.las_tunas'):
        query = cuestionario.objects.filter(entidad_codigo__ote_codigo=31, guia__activo=True)
        return query
    elif user.has_perm('guiaEstadistica.holguin'):
        query = cuestionario.objects.filter(entidad_codigo__ote_codigo=32, guia__activo=True)
        return query
    elif user.has_perm('guiaEstadistica.granma'):
        query = cuestionario.objects.filter(entidad_codigo__ote_codigo=33, guia__activo=True)
        return query
    elif user.has_perm('guiaEstadistica.santiago'):
        query = cuestionario.objects.filter(entidad_codigo__ote_codigo=34, guia__activo=True)
        return query
    elif user.has_perm('guiaEstadistica.guantanamo'):
        query = cuestionario.objects.filter(entidad_codigo__ote_codigo=35, guia__activo=True)
        return query
    elif user.has_perm('guiaEstadistica.la_isla'):
        query = cuestionario.objects.filter(entidad_codigo__ote_codigo=40, guia__activo=True)
        return query
    elif user.has_perm('guiaEstadistica.ZED_mariel'):
        query = cuestionario.objects.filter(entidad_codigo__ote_codigo=41, guia__activo=True)
        return query

# FUNCION PARA OBTENER UNA PREGUNTA DETERMINADA.
def getPregunta(codPregunta):
    query = Indicadores.objects.get(cod_indicador=codPregunta)
    return query.nombre
