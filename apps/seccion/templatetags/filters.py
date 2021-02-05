from django import template

from apps.guiaEstadistica.models import cuestionario
from apps.seccion.models import instanciaSeccion, seccion

register = template.Library()

@register.filter(name='obtenerTipo')
def obtenerTipo(clave):
        query = seccion.objects.filter(nombre=clave)
        print(query)
        return query[0].tipo


