from django.db import models
from apps.seccion.models import seccion

CHOICES = (
    ('1', 'Cadena'),
    ('2', 'Cadena_Larga'),
    ('3', 'Numerico'),
    ('4', 'Logico'),
    ('5', 'Fecha'),
    ('6', 'Fecha y Hora')

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
    tipo_dato = models.CharField(verbose_name='Tipo de dato', max_length=50,choices=CHOICES)
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


    class Meta:
        db_table = 'Nomenclador Indicadores'
        verbose_name = 'Indicador'
        verbose_name_plural = 'Indicadores'
        ordering = ['nombre']

    def __str__(self):
        return '{0}-{1}'.format(self.nombre, self.clasificadorIndicadores_id.seccion_id)


