from django.core.exceptions import ValidationError
from django.db import models
from django.forms import model_to_dict

from apps.entidad.models import Entidad
from apps.guiaEstadistica.models import guiaEstadistica, cuestionario

CHOICES_PERIODO = (
    ('Anual', 'Anual'),
    ('Trimestral', 'Trimestral')
)


CHOICES_ANO = (
    (2020, '2020'),
    (2021, '2021'),
    (2022, '2022'),
    (2023, '2023'),
    (2024, '2024'),
    (2025, '2025'),
)
CHOICE_TIPO = (
    (1,'1'),
    (2,'2'),
    (3,'3')
)
CHOICES_MESES = (
    ('Enero', 'Enero'),
    ('Febrero', 'Febrero'),
    ('Marzo', 'Marzo'),
    ('Abril', 'Abril'),
    ('Mayo', 'Mayo'),
    ('Junio', 'Junio'),
    ('Julio', 'Julio'),
    ('Agosto', 'Agosto'),
    ('Septiembre', 'Septiembre'),
    ('Octubre', 'Octubre'),
    ('Noviembre', 'Noviembre'),
    ('Diciembre', 'Diciembre')
)
class clasificadorPeriodo(models.Model):
    tipo = models.CharField('Tipo:', max_length=50, choices=CHOICES_PERIODO)
    mes_1 = models.CharField('Mes 1:', max_length=50, choices=CHOICES_MESES)
    mes_2 = models.CharField('Mes 2:', max_length=50, choices=CHOICES_MESES, blank=True, null=True)
    mes_3 = models.CharField('Mes 3:', max_length=50, choices=CHOICES_MESES, blank=True, null=True)
    ano_1 = models.IntegerField('Año:', choices=CHOICES_ANO)
    ano_2 = models.IntegerField('Año_2:', choices=CHOICES_ANO, blank=True, null=True, help_text=('Solo para el caso que el periodo sea trimestral y comience por un año y termine en otro.'))

    class Meta:
        db_table = 'Periodo'
        verbose_name = 'Periodo'
        verbose_name_plural = 'Periodos'
        ordering = ['tipo']

    def __str__(self):
        if self.tipo == 'Anual':
            return 'Periodo {0}: ({1})'.format(self.tipo, self.mes_1)
        else:
            return 'Periodo {0}: ({1},{2},{3})'.format(self.tipo, self.mes_1,self.mes_2,self.mes_3)


class seccion(models.Model):
    nombre = models.CharField(verbose_name='Nombre', max_length=255, help_text='Si el nombre de la seccion a crear contiene mas de una palabra debe poner guion bajo( _ ) entre una y la otra')
    guia_id = models.ForeignKey(guiaEstadistica,verbose_name='Guia a vincular', blank=True, null=True, on_delete=models.CASCADE)
    periodo_id = models.ForeignKey(clasificadorPeriodo,verbose_name='Periodo a controlar', blank=True, null=True, on_delete=models.CASCADE)
    numero = models.CharField(verbose_name='Numero',max_length=5, blank=True, null=True)
    subNumero = models.CharField(verbose_name='Sub-numero', max_length=5, blank=True, null=True)
    orden = models.IntegerField(verbose_name='Orden', blank=True, null=True)
    activo = models.BooleanField(verbose_name='Es_activo', default=True, blank=True, null=True)
    tipo = models.IntegerField(verbose_name='Tipo de seccion', choices=CHOICE_TIPO, blank=True, null=True)




    class Meta:
        db_table = 'Seccion'
        verbose_name = 'Seccion'
        verbose_name_plural = 'Secciones'
        ordering = ['orden']

    def __str__(self):
        return '{0}-guia {1}'.format(self.nombre, self.guia_id.nombre)

    def toJSON(self):
        item = model_to_dict(self)
        return item



class nomencladorCodigo(models.Model):
    codigo = models.CharField(verbose_name='Codigo a controlar',max_length=5, unique=True, blank=True, null=True)
    descripcion = models.CharField(verbose_name='Descripcion', max_length=150)
    activo = models.BooleanField(verbose_name='Es_activo', default=True)


    class Meta:
        db_table = 'Nomenclador Codigo'
        verbose_name = 'Nomenclador Codigo'
        verbose_name_plural = 'Nomenclador Codigos'
        ordering = ['codigo']

    def __str__(self):
        return 'Codigo ' + str(self.codigo)


class nomencladorColumna(models.Model):
    seccion_id = models.ForeignKey(seccion,verbose_name='Seccion a vincular', on_delete=models.CASCADE, blank=True, null=True)
    codigo_id = models.ManyToManyField(nomencladorCodigo, verbose_name='Codigo/Codigos a controlar')
    columna = models.CharField(max_length=5, blank=True, null=True, verbose_name='Columna a controlar')
    descripcion = models.CharField(max_length=150, verbose_name='Descripcion')
    activo = models.BooleanField(default=True, verbose_name='Es_activo')


    class Meta:
        db_table = 'Nomenclador Columna'
        verbose_name = 'Nomenclador Columna'
        verbose_name_plural = 'Nomenclador Columnas'
        ordering = ['columna']

    def __str__(self):
        return 'Columna {0}: {1}, (secion-{2}, guia-{3})'.format(str(self.columna), self.descripcion, self.seccion_id.nombre, self.seccion_id.guia_id.nombre)

    def toJSON(self):
        item = model_to_dict(self)
        return item

class instanciaSeccion(models.Model):
    seccion_id = models.ForeignKey(seccion, on_delete=models.CASCADE, blank=True, null=True)
    cuestionario_fk = models.ForeignKey(cuestionario, on_delete=models.CASCADE, blank=True, null=True)
    codigo_id = models.ForeignKey(nomencladorCodigo, on_delete=models.CASCADE, blank=True, null=True)
    columna_id = models.ForeignKey(nomencladorColumna, on_delete=models.CASCADE, blank=True, null=True)
    modelo_1 = models.DecimalField(' Asignado el primer mes.', blank=True, null=True,
                                   decimal_places=2, max_digits=15)
    modelo_2 = models.DecimalField(' Asignado el segundo mes.', blank=True, null=True,
                                   decimal_places=2, max_digits=15)
    modelo_3 = models.DecimalField(' Asignado el tercer mes.', blank=True, null=True,
                                   decimal_places=2, max_digits=15)
    registro_1 = models.DecimalField(' Registro real del primer mes a controlar.', blank=True, null=True,
                                     decimal_places=2, max_digits=15)
    registro_2 = models.DecimalField(' Registro real del segundo mes a controlar..', blank=True, null=True,
                                     decimal_places=2, max_digits=15)
    registro_3 = models.DecimalField(' Registro real del tercer mes a controlar.', blank=True, null=True,
                                     decimal_places=2, max_digits=15)

    class Meta:
        db_table = 'Instancia Seccion'
        verbose_name = 'Instancia de la seccion'
        verbose_name_plural = 'Instancias de las secciones'
        ordering = ['id']

    def clean(self):
        if self.modelo_1 == -1:
            print('error')
            raise ValidationError('error')

    def __str__(self):
        return 'Insntacia de la {0}'.format(self.seccion_id)

    def get_diferencia_1(self):
        diferencia = self.modelo_1 - self.registro_1
        return diferencia

    def get_diferencia_2(self):
        diferencia = self.modelo_2 - self.registro_2
        return diferencia

    def get_diferencia_3(self):
        diferencia = self.modelo_3 - self.registro_3
        return diferencia

    def toJSON(self):
        item = model_to_dict(self)
        item['seccion_id'] = self.seccion_id.nombre
        item['numero'] = self.seccion_id.numero
        item['codigo_id'] = self.codigo_id.codigo
        item['columna_id'] = self.columna_id.columna
        item['modelo_1'] = self.modelo_1
        item['registro_1'] = self.registro_1
        item['modelo_2'] = self.modelo_2
        item['registro_2'] = self.registro_2
        item['modelo_3'] = self.modelo_3
        item['registro_3'] = self.registro_3
        item['diferencia_1'] = self.get_diferencia_1()
        item['diferencia_2'] = self.get_diferencia_2()
        item['diferencia_3'] = self.get_diferencia_3()
        return item


class verificacion(models.Model):
    seccion_id = models.ForeignKey(seccion, on_delete=models.CASCADE, blank=True, null=True)
    cuestionario_fk = models.ForeignKey(cuestionario, on_delete=models.CASCADE, blank=True, null=True)
    indicadoresVerificados = models.IntegerField('Cantidad de indicadores verificados', default=0, blank=True, null=True)
    indicadoresIncluidos = models.CharField(
        verbose_name='Estan incluidos en la informacion todos los establecimientos ?',
        blank=True, null=True,
        max_length=2)
    indicadoresCoinciden = models.IntegerField('Cuantos coinciden ?', default=0, blank=True, null=True)

    class Meta:
        db_table = 'Verificacion'
        verbose_name = 'Verificacion'
        verbose_name_plural = 'Verificaciones'
        ordering = ['id']

    def __str__(self):
        return 'Verificacion de la  seccion {0} a la entidad {1}'.format(self.seccion_id.nombre, self.cuestionario_fk.entidad_codigo.nombre_CI)


    def toJSON(self):
        item = model_to_dict(self)
        return item