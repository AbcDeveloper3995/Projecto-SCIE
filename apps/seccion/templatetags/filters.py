from django import template

import utils

from apps.guiaEstadistica.models import cuestionario, PreguntasEvaluadas
from apps.indicadores.models import Indicadores
from apps.seccion.models import seccion, verificacion

register = template.Library()

# FILTRO PARA OBTENER EL TIPO DE SECCION.
@register.filter(name='obtenerTipo')
def obtenerTipo(clave):
        query = seccion.objects.filter(nombre=clave)
        print(query)
        return query[0].tipo

# FILTRO PARA OBTENER EL TOTAL DE CUESTIONARIOS.
@register.filter(name='totalCuestionarios')
def totalCuestionarios(user):
        query = cuestionario.objects.all().count()
        return query

# FILTRO PARA OBTENER EL NUMERO DE LA SECCION.
@register.filter(name='numeroSeccion')
def numeroSeccion(Seccion):
        query = seccion.objects.get(nombre=Seccion)
        return query.numero

# FILTRO PARA OBTENER EL TOTAL DE INDICADORES VERIFICADOS QUE NO COINCIDEN.
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

# FILTRO PARA OBTENER EL PORCIENTO QUE REPRESENTA LOS QUE NO COINCIDEN DEL TOTAL.
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

# FILTRO PARA OBTENER EL LA CATIDAD DE PREGUNTAS DE UN GRUPO DE PREGUNTAS.
@register.filter(name='cantDepreguntas')
def cantDepreguntas(idGrupoPregunta):
        query = Indicadores.objects.filter(clasificadorIndicadores_id__id=idGrupoPregunta).count()
        return query

# FILTRO PARA OBTENER LAS PREGUNTAS DE UN GRUPO DE PREGUNTAS.
@register.filter(name='preguntas')
def preguntas(idGrupoPregunta):
    query = Indicadores.objects.filter(clasificadorIndicadores_id__id=idGrupoPregunta)
    return query

# FILTRO PARA OBTENER LAS PREGUNTAS EVALUADAS DE UN CUESTIONARIO A PARTIR DE LA POSICION 4 EN ADELANTE.
@register.filter(name='respuestas')
def preguntas(Cuestionario):
    query = PreguntasEvaluadas.objects.filter(captacion_id__id=Cuestionario.id)[4:]
    return query

# FILTRO PARA OBTENER EL TOTAL DE CADA PREGUNTA DE DISCIPLINA INFORMATIVA ENTRE TODAS LAS ENTIDADES.
@register.filter(name='procedimientoTotalDiscplinaInfo')
def determinarTotales(user,codPeticion):
    query = utils.getCuestionarios(user)
    if codPeticion == 1:
        pregunta = utils.getPregunta(31)
        totalReportar = getTotal(query,pregunta)
        return totalReportar
    elif codPeticion == 2:
        pregunta = utils.getPregunta(32)
        totalReportar = getTotal(query, pregunta)
        return totalReportar
    elif codPeticion == 3:
        pregunta = utils.getPregunta(33)
        totalReportar = getTotal(query, pregunta)
        return totalReportar
    elif codPeticion == 4:
        pregunta = utils.getPregunta(34)
        totalReportar = getTotal(query, pregunta)
        return totalReportar

def getTotal(listaCuestionario, nombrePregunta):
    total = 0
    for i in listaCuestionario :
        query = PreguntasEvaluadas.objects.get(captacion_id__id=i.id, pregunta=nombrePregunta)
        total+=int(query.respuesta)
    return total

# FILTRO PARA OBTENER EL VALOR DE CADA PREGUNTA DE DISCIPLINA INFORMATIVA DE CADA ENTIDAD.
@register.filter(name='discplinaInfoEntidad')
def determinarRespuesta(cuestionario,codPeticion):
    if codPeticion == 1:
        pregunta = utils.getPregunta(31)
        totalReportar = getRespuesta(cuestionario,pregunta)
        return totalReportar
    elif codPeticion == 2:
        pregunta = utils.getPregunta(32)
        totalReportar = getRespuesta(cuestionario, pregunta)
        return totalReportar
    elif codPeticion == 3:
        pregunta = utils.getPregunta(33)
        totalReportar = getRespuesta(cuestionario, pregunta)
        return totalReportar
    elif codPeticion == 4:
        pregunta = utils.getPregunta(34)
        totalReportar = getRespuesta(cuestionario,pregunta)
        return totalReportar

def getRespuesta(cuestionario, nombrePregunta):
    query = PreguntasEvaluadas.objects.get(captacion_id__id=cuestionario.id, pregunta=nombrePregunta)
    return query.respuesta

# FILTRO PARA OBTENER LOS SENALAMIENTOS DE CADA ENTIDAD.
@register.filter(name='senalamientos')
def getSenalamientos(cuestionario):
    pregunta = utils.getPregunta(42)
    respuesta = getRespuesta(cuestionario, pregunta)
    return respuesta

# FILTRO PARA OBTENER EL TOTAL LOS SENALAMIENTOS ENTRE TODAS LAS ENTIDAD.
@register.filter(name='totalsenalamientos')
def determinarTotales(user):
    query = utils.getCuestionarios(user)
    pregunta = utils.getPregunta(42)
    totalReportar = getTotal(query, pregunta)
    return totalReportar

# FILTRO PARA OBTENER LAS ENTIDADES CON EL DOMICILIO SOCIAL INCORRECTO.
@register.filter(name='domicilioIncorrecto')
def getDomicilioIncorrecto(cuestionario):
    pregunta = utils.getPregunta(15)
    respuesta = getRespuesta(cuestionario, pregunta)
    return respuesta

