from django.db import models
from django.forms import model_to_dict

from apps.entidad.models import Entidad

CHOICES_INDICADOR = (
    ('Si', 'Si'),
    ('No', 'No')
)

class guiaEstadistica(models.Model):
    nombre = models.CharField(verbose_name='Control integral a', max_length=255)
    fecha_inicio = models.DateField(verbose_name='Fecha de apeturar', auto_now=True)
    fecha_fin = models.DateField(verbose_name='Fecha de cierre', auto_now_add=True)
    activo = models.BooleanField(verbose_name='Es_activo', default=True)

    class Meta:
        db_table = 'Guia Estadistica'
        verbose_name = 'Guia Estadistica'
        verbose_name_plural = 'Guias Estadisticas'
        ordering = ['nombre']

    def toJSON(self):
        item = model_to_dict(self)
        return item

    def __str__(self):
        return 'Guia Estadistica aplicada a: ' + self.nombre

class universoEntidades(models.Model):
    guia = models.ForeignKey(guiaEstadistica, verbose_name='Guia', blank=True, null=True, on_delete=models.CASCADE)
    entidad_codigo = models.ForeignKey(Entidad, verbose_name='Entidades que se le aplicara la guia', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'UniversoEntidades'
        verbose_name = 'Universo'
        verbose_name_plural = 'Universo'

    def __str__(self):
        return "{0}, {1}".format(str(self.guia), self.entidad_codigo)

class cuestionario(models.Model):
    guia = models.ForeignKey(guiaEstadistica, verbose_name='Guia', blank=True, null=True, on_delete=models.CASCADE)
    entidad_codigo = models.OneToOneField(Entidad, verbose_name='Entidad controlada', blank=True,
                                       null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Cuestionario'
        verbose_name = 'Cuestionario'
        verbose_name_plural = 'Cuestionarios'


    def __str__(self):
        return 'Captacion: {0} de la guia {1}'.format(self.id, self.guia.nombre)




