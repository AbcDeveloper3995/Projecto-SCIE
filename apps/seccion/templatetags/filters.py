from django import template

from apps.guiaEstadistica.models import cuestionario, PreguntasEvaluadas
from apps.indicadores.models import Indicadores
from apps.seccion.models import seccion, verificacion

register = template.Library()


@register.filter(name='obtenerTipo')
def obtenerTipo(clave):
        query = seccion.objects.filter(nombre=clave)
        print(query)
        return query[0].tipo

@register.filter(name='totalCuestionarios')
def totalCuestionarios(user):
        query = cuestionario.objects.all().count()
        return query

@register.filter(name='numeroSeccion')
def numeroSeccion(Seccion):
        query = seccion.objects.get(nombre=Seccion)
        return query.numero

@register.filter(name='verificadosNoCoinciden')
def verificadosNoCoinciden(seccion):
        verificados = 0
        coinciden = 0
        query = verificacion.objects.filter(seccion_id__nombre=seccion)
        for j in query:
           verificados += j.indicadoresVerificados
           coinciden +=j.indicadoresCoinciden
        noCoinciden = verificados-coinciden
        return noCoinciden

@register.filter(name='porciento')
def porciento(seccion):
        verificados = 0
        coinciden = 0
        query = verificacion.objects.filter(seccion_id__nombre=seccion)
        for j in query:
           verificados += j.indicadoresVerificados
           coinciden +=j.indicadoresCoinciden
        noCoinciden = verificados-coinciden
        if noCoinciden == 0:
           return 0
        else:
           porciento = noCoinciden*100//verificados
           return porciento

@register.filter(name='cantDepreguntas')
def cantDepreguntas(idGrupoPregunta):
        query = Indicadores.objects.filter(clasificadorIndicadores_id__id=idGrupoPregunta).count()
        print(query)
        return query

@register.filter(name='preguntas')
def preguntas(idGrupoPregunta):
    query = Indicadores.objects.filter(clasificadorIndicadores_id__id=idGrupoPregunta)
    return query

@register.filter(name='respuestas')
def preguntas(Cuestionario):
    query = PreguntasEvaluadas.objects.filter(captacion_id__id=Cuestionario.id)[4:]
    return query

@register.filter(name='procedimientoDiscplinaInfo')
def getCuestionarios(user,codPeticion):
    if user.is_superuser:
        query = cuestionario.objects.all()
        if codPeticion == 1:
            pregunta = getPregunta31()
            totalReportar = getTotal(query,pregunta)
            return totalReportar
        elif codPeticion == 2:
            pregunta = getPregunta32()
            totalReportar = getTotal(query, pregunta)
            return totalReportar
        elif codPeticion == 3:
            pregunta = getPregunta33()
            totalReportar = getTotal(query, pregunta)
            return totalReportar
        elif codPeticion == 4:
            pregunta = getPregunta34()
            totalReportar = getTotal(query, pregunta)
            return totalReportar

    elif user.has_perm('guiaEstadistica.pinar'):
        query = cuestionario.objects.filter(entidad_codigo__ote_codigo=21, guia__activo=True)
        return query
    elif user.has_perm('guiaEstadistica.habana'):
        query = cuestionario.objects.filter(entidad_codigo__ote_codigo=23, guia__activo=True)
        return query

def getPregunta31():
    query = Indicadores.objects.get(cod_indicador=31)
    return query.nombre
def getPregunta32():
    query = Indicadores.objects.get(cod_indicador=32)
    return query.nombre
def getPregunta33():
    query = Indicadores.objects.get(cod_indicador=33)
    return query.nombre
def getPregunta34():
    query = Indicadores.objects.get(cod_indicador=34)
    return query.nombre

def getTotal(listaCuestionario, nombrePregunta):
    total = 0
    for i in listaCuestionario :
        query = PreguntasEvaluadas.objects.get(captacion_id__id=i.id, pregunta=nombrePregunta)
        total+=int(query.respuesta)
    return total


