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