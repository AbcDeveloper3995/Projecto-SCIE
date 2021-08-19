from django.db import models
from django.forms import model_to_dict

from apps.guiaEstadistica.models import cuestionario
from apps.seccion.models import seccion

CHOICES = (
    ('1', 'Cadena'),
    ('2', 'Cadena_Larga'),
    ('3', 'Numerico'),
    ('4', 'Logico'),
    ('5', 'Fecha'),

)

class clasificadorIndicadores(models.Model):
    seccion_id = models.ForeignKey(seccion,verbose_name='Seccion a vincular', blank=True, null=True, on_delete=models.CASCADE)
    nombre = models.CharField(verbose_name='Nombre', max_length=255, blank=False, null=False)
    activo = models.BooleanField(verbose_name='Es_activo', default=True)

    class Meta:
        db_table = 'Clasificador Indicador'
        verbose_name = 'Clasificador indicador'
        verbose_name_plural = 'Clasificador indicadores'
        ordering = ['nombre']

    def __str__(self):
        return '{0}-{1}'.format(self.nombre, self.seccion_id)

class posiblesRespuestas(models.Model):
    nombre = models.CharField(verbose_name='Nombre', max_length=50, blank=False, null=False, unique=True)
    tipo_dato = models.CharField(verbose_name='Tipo de respuesta', max_length=50,choices=CHOICES)
    activo = models.BooleanField(verbose_name='Es_activo', default=True)


    class Meta:
        db_table = 'Posibles Respuestas'
        verbose_name = 'Posible respuesta'
        verbose_name_plural = 'Posibles respuestas'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Indicadores(models.Model):
    clasificadorIndicadores_id = models.ForeignKey(clasificadorIndicadores,verbose_name='Grupo de pregunta a vincular', blank=True, null=True, on_delete=models.CASCADE)
    respuestas_id = models.ManyToManyField(posiblesRespuestas,verbose_name='Posibles respuestas', blank=True, null=True)
    nombre = models.CharField(verbose_name='Nombre', max_length=255, blank=False, null=False)
    activo = models.BooleanField(verbose_name='Es_activo', default=True)
    cod_indicador = models.IntegerField(verbose_name='Codigo de pregunta', blank=True, null=True)
    fechaCreacion = models.DateField(verbose_name='Fecha de creacion', auto_now=True, blank=True, null=True)


    class Meta:
        db_table = 'Nomenclador Indicadores'
        verbose_name = 'Indicador'
        verbose_name_plural = 'Indicadores'
        ordering = ['fechaCreacion']

    def __str__(self):
        return '{0}-{1}'.format(self.nombre, self.clasificadorIndicadores_id.seccion_id)


class PreguntasEvaluadas(models.Model):
    captacion_id = models.ForeignKey(cuestionario,verbose_name='Cuestionario', blank=True, null=True, on_delete=models.CASCADE)
    pregunta = models.ForeignKey(Indicadores,verbose_name='Preguntas', blank=True, null=True, on_delete=models.CASCADE)
    respuesta = models.CharField(verbose_name='Respuesta', max_length=250, blank=True, null=True)

    class Meta:
        db_table = 'PreguntasEvaluadas'
        verbose_name = 'Preguntas Evaluadas'
        verbose_name_plural = 'Preguntas Evaluadas'


    def __str__(self):
        return 'Pregunta evaluada: {0}'.format(self.pregunta)

    def toJSON(self):
        item = model_to_dict(self)
        return item