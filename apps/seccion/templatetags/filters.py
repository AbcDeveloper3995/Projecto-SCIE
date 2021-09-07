from django import template

import utils
from apps.guiaEstadistica.models import cuestionario
from apps.indicadores.models import Indicadores, PreguntasEvaluadas
from apps.seccion.models import seccion, verificacion

register = template.Library()

# FILTRO PARA OBTENER EL TIPO DE SECCION.
@register.filter(name='obtenerTipo')
def obtenerTipo(clave):
        query = seccion.objects.filter(nombre=clave)
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

'''REPORTE DE VERIFICACIONES'''

'''Esta parte es para trabajar con las infomacion de las verificaciones de manera general'''

# FILTRO PARA OBTENER EL TOTAL DE INDICADORES VERIFICADOS QUE NO COINCIDEN.

@register.filter(name='totalVerificados')
def totalVerificados(user, nombreSeccion):
        verificados = 0
        cuestionarios = utils.getCuestionarios(user)
        for i in cuestionarios:
            query = verificacion.objects.filter(seccion_id__nombre=nombreSeccion, cuestionario_fk=i)
            if query.count() != 0:
                for j in query:
                    verificados += j.indicadoresVerificados
            else:
                verificados += 0
        return verificados


@register.filter(name='totalVerificadosNoCoinciden')
def totalVerificadosNoCoinciden(user, nombreSeccion):
        verificados = totalVerificados(user,nombreSeccion)
        coinciden = 0
        cuestionarios = utils.getCuestionarios(user)
        for i in cuestionarios:
            query = verificacion.objects.filter(seccion_id__nombre=nombreSeccion, cuestionario_fk=i)
            if query.count() != 0:
                for j in query:
                    coinciden +=j.indicadoresCoinciden
            else:
                coinciden += 0
        noCoinciden = verificados - coinciden
        return noCoinciden

# FILTRO PARA OBTENER EL PORCIENTO QUE REPRESENTA LOS QUE NO COINCIDEN DEL TOTAL.
@register.filter(name='totalPorciento')
def totalPorciento(user, nombreSeccion):
        verificados = totalVerificados(user,nombreSeccion)
        noCoinciden = totalVerificadosNoCoinciden(user, nombreSeccion)
        if noCoinciden == 0:return 0
        porciento = noCoinciden*100//verificados
        return porciento

'''Esta otra parte es para trabajar con las infomacion de las verificaciones de cada cuestionario captado'''

# FILTRO PARA OBTENER LA CANTIDAD INDICADORES VERIFICADOS DE UN CENTRO INFORMANTE.
@register.filter(name='verificados')
def getInfoVerificacion(cuestionarioId, seccion):
    try:
        query = verificacion.objects.get(cuestionario_fk__id=cuestionarioId, seccion_id__nombre=seccion)
        return query.indicadoresVerificados
    except:
        return None

# FILTRO PARA OBTENER LA CANTIDAD DE INDICADORES VERIFICADOS  DE UN CENTRO INFORMANTE QUE NO COINCIDEN.
@register.filter(name='noCoinciden')
def getInfoVerificacion(cuestionarioId, seccion):
    try:
        query = verificacion.objects.get(cuestionario_fk__id=cuestionarioId, seccion_id__nombre=seccion)
        noCoinciden = query.indicadoresVerificados - query.indicadoresCoinciden
        return noCoinciden
    except:
        return 'no existe'

# FILTRO PARA OBTENER EL % QUE REPRESENTA LOS QUE NO COINCIDEN DE LOS VERIFICADOS.
@register.filter(name='porcientoVerificacion')
def getInfoVerificacion(cuestionarioId, seccion):
    try:
        query = verificacion.objects.get(cuestionario_fk__id=cuestionarioId, seccion_id__nombre=seccion)
        noCoinciden = query.indicadoresVerificados - query.indicadoresCoinciden
        porciento = int(noCoinciden*100/query.indicadoresVerificados)
        return porciento
    except:
        return None

#**********************************************************************************************************

# FILTRO PARA OBTENER EL LA CATIDAD DE PREGUNTAS DE UN GRUPO DE PREGUNTAS.
@register.filter(name='cantDepreguntas')
def cantDepreguntas(idGrupoPregunta):
        query = Indicadores.objects.filter(clasificadorIndicadores_id__id=idGrupoPregunta).count()
        return query

# FILTRO PARA OBTENER LAS PREGUNTAS DE UN GRUPO DE PREGUNTAS.
@register.filter(name='preguntas')
def preguntas(idGrupoPregunta):
    query = Indicadores.objects.filter(clasificadorIndicadores_id__id=idGrupoPregunta)[::-1]
    return query

# FILTRO PARA OBTENER LAS PREGUNTAS EVALUADAS DE UN CUESTIONARIO A PARTIR DE LA POSICION 4 EN ADELANTE.
@register.filter(name='respuestas')
def respuestas(idGrupoPregunta,Cuestionario):
    respuestas = []
    preguntas = Indicadores.objects.filter(clasificadorIndicadores_id__id=idGrupoPregunta)[::-1]
    for i in preguntas:
        query = PreguntasEvaluadas.objects.get(captacion_id__id=Cuestionario.id, pregunta=i)
        respuestas.append(query.respuesta)
    return respuestas

# FILTRO PARA OBTENER EL TOTAL DE CADA PREGUNTA DE DISCIPLINA INFORMATIVA ENTRE TODAS LAS ENTIDADES.
@register.filter(name='procedimientoTotalDiscplinaInfo')
def determinarTotales(user,codPeticion):
    query = utils.getCuestionarios(user)
    if codPeticion == 1:
        pregunta = utils.getPregunta(31)
        totalReportar = getTotal(query, pregunta)
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

def getTotal(listaCuestionario, pregunta):
    total = 0
    for i in listaCuestionario :
        query = PreguntasEvaluadas.objects.get(captacion_id__id=i.id, pregunta_id=pregunta.id)
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

def getRespuesta(cuestionario, pregunta):
    query = PreguntasEvaluadas.objects.get(captacion_id__id=cuestionario.id, pregunta_id=pregunta.id)
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


# FILTRO PARA OBTENER LAS ENTIDADES CON EL DOMICILIO SOCIAL INCORRECTO.
@register.filter(name='progreso')
def progreso(cuestionario, cantSecciones):
    porcentaje = 2 * 100 // cantSecciones
    try:
        query = verificacion.objects.filter(cuestionario_fk=cuestionario).count()
        if query == 0:
            return porcentaje
        else:
            porcentaje += query*100//cantSecciones
            return porcentaje
    except:
        print('error progreso')
