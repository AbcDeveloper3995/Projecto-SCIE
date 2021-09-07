from apps.guiaEstadistica.models import cuestionario, universoEntidades
from apps.indicadores.models import Indicadores

# FUNCION PARA OBTENER EL UNIVERSO AL CUAL SE LE VA HA APLICAR LA GUIA, TENIENDO EN CUENTA LOS PERMISOS DE USUARIOS.
def getUniverso(user):
    if user.has_perm('usuario.administrador') or user.has_perm('usuario.estadistico'):
        query = universoEntidades.objects.all()
        return query
    elif user.has_perm('usuario.pinar'):
        query = universoEntidades.objects.filter(entidad_codigo__ote_codigo=21, guia__activo=True)
        return query
    elif user.has_perm('usuario.artemisa'):
        query = universoEntidades.objects.filter(entidad_codigo__ote_codigo=22, guia__activo=True)
        return query
    elif user.has_perm('usuario.habana'):
        query = universoEntidades.objects.filter(entidad_codigo__ote_codigo=23, guia__activo=True)
        return query
    elif user.has_perm('usuario.mayabeque'):
        query = universoEntidades.objects.filter(entidad_codigo__ote_codigo=24, guia__activo=True)
        return query
    elif user.has_perm('usuario.matanzas'):
        query = universoEntidades.objects.filter(entidad_codigo__ote_codigo=25, guia__activo=True)
        return query
    elif user.has_perm('usuario.villa_clara'):
        query = universoEntidades.objects.filter(entidad_codigo__ote_codigo=26, guia__activo=True)
        return query
    elif user.has_perm('usuario.cienfuegos'):
        query = universoEntidades.objects.filter(entidad_codigo__ote_codigo=27, guia__activo=True)
        return query
    elif user.has_perm('usuario.santi_spiritu'):
        query = universoEntidades.objects.filter(entidad_codigo__ote_codigo=28, guia__activo=True)
        return query
    elif user.has_perm('usuario.ciego'):
        query = universoEntidades.objects.filter(entidad_codigo__ote_codigo=29, guia__activo=True)
        return query
    elif user.has_perm('usuario.camaguey'):
        query = universoEntidades.objects.filter(entidad_codigo__ote_codigo=30, guia__activo=True)
        return query
    elif user.has_perm('usuario.las_tunas'):
        query = universoEntidades.objects.filter(entidad_codigo__ote_codigo=31, guia__activo=True)
        return query
    elif user.has_perm('usuario.holguin'):
        query = universoEntidades.objects.filter(entidad_codigo__ote_codigo=32, guia__activo=True)
        return query
    elif user.has_perm('usuario.granma'):
        query = universoEntidades.objects.filter(entidad_codigo__ote_codigo=33, guia__activo=True)
        return query
    elif user.has_perm('usuario.santiago'):
        query = universoEntidades.objects.filter(entidad_codigo__ote_codigo=34, guia__activo=True)
        return query
    elif user.has_perm('usuario.guantanamo'):
        query = universoEntidades.objects.filter(entidad_codigo__ote_codigo=35, guia__activo=True)
        return query
    elif user.has_perm('usuario.la_isla'):
        query = universoEntidades.objects.filter(entidad_codigo__ote_codigo=40, guia__activo=True)
        return query
    elif user.has_perm('usuario.ZED_mariel'):
        query = universoEntidades.objects.filter(entidad_codigo__ote_codigo=41, guia__activo=True)
        return query

# FUNCION PARA OBTENER UN LISTADO DE CUESTIONARIOS SEGUN EL PERMISO DEL USUARIO.
def getCuestionarios(user):
    if user.has_perm('usuario.administrador') or user.has_perm('usuario.estadistico'):
        query = cuestionario.objects.all()
        return query
    elif user.has_perm('usuario.pinar'):
        query = cuestionario.objects.filter(entidad_codigo__ote_codigo=21, guia__activo=True)
        return query
    elif user.has_perm('usuario.artemisa'):
        query = cuestionario.objects.filter(entidad_codigo__ote_codigo=22, guia__activo=True)
        return query
    elif user.has_perm('usuario.habana'):
        query = cuestionario.objects.filter(entidad_codigo__ote_codigo=23, guia__activo=True)
        return query
    elif user.has_perm('usuario.mayabeque'):
        query = cuestionario.objects.filter(entidad_codigo__ote_codigo=24, guia__activo=True)
        return query
    elif user.has_perm('usuario.matanzas'):
        query = cuestionario.objects.filter(entidad_codigo__ote_codigo=25, guia__activo=True)
        return query
    elif user.has_perm('usuario.villa_clara'):
        query = cuestionario.objects.filter(entidad_codigo__ote_codigo=26, guia__activo=True)
        return query
    elif user.has_perm('usuario.cienfuegos'):
        query = cuestionario.objects.filter(entidad_codigo__ote_codigo=27, guia__activo=True)
        return query
    elif user.has_perm('usuario.santi_spiritu'):
        query = cuestionario.objects.filter(entidad_codigo__ote_codigo=28, guia__activo=True)
        return query
    elif user.has_perm('usuario.ciego'):
        query = cuestionario.objects.filter(entidad_codigo__ote_codigo=29, guia__activo=True)
        return query
    elif user.has_perm('usuario.camaguey'):
        query = cuestionario.objects.filter(entidad_codigo__ote_codigo=30, guia__activo=True)
        return query
    elif user.has_perm('usuario.las_tunas'):
        query = cuestionario.objects.filter(entidad_codigo__ote_codigo=31, guia__activo=True)
        return query
    elif user.has_perm('usuario.holguin'):
        query = cuestionario.objects.filter(entidad_codigo__ote_codigo=32, guia__activo=True)
        return query
    elif user.has_perm('usuario.granma'):
        query = cuestionario.objects.filter(entidad_codigo__ote_codigo=33, guia__activo=True)
        return query
    elif user.has_perm('usuario.santiago'):
        query = cuestionario.objects.filter(entidad_codigo__ote_codigo=34, guia__activo=True)
        return query
    elif user.has_perm('usuario.guantanamo'):
        query = cuestionario.objects.filter(entidad_codigo__ote_codigo=35, guia__activo=True)
        return query
    elif user.has_perm('usuario.la_isla'):
        query = cuestionario.objects.filter(entidad_codigo__ote_codigo=40, guia__activo=True)
        return query
    elif user.has_perm('usuario.ZED_mariel'):
        query = cuestionario.objects.filter(entidad_codigo__ote_codigo=41, guia__activo=True)
        return query

# FUNCION PARA OBTENER UNA PREGUNTA DETERMINADA.
def getPregunta(codPregunta):
    query = Indicadores.objects.get(cod_indicador=codPregunta)
    return query

def getLastCuestionario():
    return cuestionario.objects.last()
