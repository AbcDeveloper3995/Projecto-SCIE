from apps.guiaEstadistica.models import cuestionario
from apps.indicadores.models import Indicadores


def getCuestionarios(user):
    if user.is_superuser:
        query = cuestionario.objects.all()
        return query
    elif user.has_perm('guiaEstadistica.pinar'):
        query = cuestionario.objects.filter(entidad_codigo__ote_codigo=21, guia__activo=True)
        return query
    elif user.has_perm('guiaEstadistica.habana'):
        query = cuestionario.objects.filter(entidad_codigo__ote_codigo=23, guia__activo=True)
        return query

def getPregunta(codPregunta):
    query = Indicadores.objects.get(cod_indicador=codPregunta)
    return query.nombre
