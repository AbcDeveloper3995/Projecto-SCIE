from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.forms import model_to_dict

# Los campos codigos estan de tipo charfield para que pueda ingresar codigos que empiecen con 0 EJ: 012345

class organismo(models.Model):
    codigo = models.CharField(verbose_name='Codigo', max_length=5, unique=True,  blank=False, null=False)
    descripcion = models.CharField(verbose_name='Descripcion', max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'Organismo'
        verbose_name = 'COrganismo'
        verbose_name_plural = 'Organismo'
        ordering = ['codigo']

    def __str__(self):
        return str(self.codigo)

class osde(models.Model):
    codigo = models.CharField(verbose_name='Codigo', max_length=10, unique=True,  blank=False, null=False)
    descripcion = models.CharField(verbose_name='Descripcion', max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'OSDE'
        verbose_name = 'OSDE'
        verbose_name_plural = 'OSDE'
        ordering = ['codigo']

    def __str__(self):
        return str(self.codigo)


class clasificadorDPA(models.Model):
    codigo = models.IntegerField(verbose_name='Codigo', unique=True,  blank=False, null=False)
    descripcion = models.CharField(verbose_name='Descripcion', max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'Clasificador_DPA'
        verbose_name = 'Clasificador_DPA'
        verbose_name_plural = 'Clasificador_DPA'
        ordering = ['codigo']

    def __str__(self):
        return str(self.codigo)


class clasificadorNAE(models.Model):
    codigo = models.CharField(verbose_name='Codigo', max_length=5, unique=True, blank=False, null=False)
    descripcion = models.CharField(verbose_name='Descripcion', max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'Clasificador_NAE'
        verbose_name = 'Clasificador_NAE'
        verbose_name_plural = 'Clasificador_NAE'
        ordering = ['codigo']

    def __str__(self):
        return str(self.codigo)

class Entidad(models.Model):
    codigo_CI = models.CharField(verbose_name='Codigo Centro Informante', max_length=15, unique=True, blank=False, null=False)
    nombre_CI = models.CharField(verbose_name='Nombre Centro Informante', max_length=150, blank=False, null=False)
    ote_codigo = models.ForeignKey(clasificadorDPA, verbose_name='Provincia', blank=True, null=True, related_name='provincia', on_delete=models.CASCADE)
    ome_codigo = models.ForeignKey(clasificadorDPA, verbose_name='Municipio', blank=True, null=True, related_name='municipio', on_delete=models.CASCADE)
    codigo_NAE = models.ForeignKey(clasificadorNAE, verbose_name='Codigo NAE', blank=True, null=True, on_delete=models.CASCADE)
    org_codigo = models.ForeignKey(organismo, verbose_name='Codigo ORGANISMO', blank=True, null=True, on_delete=models.CASCADE)
    osde_codigo = models.ForeignKey(osde, verbose_name='Codigo OSDE', blank=True, null=True, on_delete=models.CASCADE)


    class Meta:
        db_table = 'Entidad'
        verbose_name = 'Entidad'
        verbose_name_plural = 'Entidades'
        ordering = ['codigo_CI']

    def getCodigoNae(self):
        try:
            if self.codigo_NAE:return self.codigo_NAE.codigo
            else:return '999'
        except ObjectDoesNotExist:
            return '999'

    def getDescripcionNae(self):
        try:
            if self.codigo_NAE:return self.codigo_NAE.descripcion
            else:return 'DESCONOCIDO'
        except ObjectDoesNotExist:
            return 'DESCONOCIDO'

    def getCodigoOrg(self):
        try:
            if self.org_codigo:return self.org_codigo.codigo
            else:return '999'
        except ObjectDoesNotExist:
            return '999'

    def getDescripcionOrg(self):
        try:
            if self.org_codigo:return self.org_codigo.descripcion
            else: return 'DESCONOCIDO'
        except ObjectDoesNotExist:
            return 'DESCONOCIDO'

    def getCodigoOsde(self):
        try:
            if self.osde_codigo:return self.osde_codigo.codigo
            else:return '999'
        except ObjectDoesNotExist:
            return '999'

    def getDescripcionOsde(self):
        try:
            if self.osde_codigo: return self.osde_codigo.descripcion
            else: return 'DESCONOCIDO'
        except ObjectDoesNotExist:
            return 'DESCONOCIDO'

    def toJSON(self):
        item = model_to_dict(self)
        item['codigo_CI'] = self.codigo_CI
        item['nombre_CI'] = self.nombre_CI
        item['ome_codigo'] = self.ome_codigo.codigo
        item['ome_descripcion'] = self.ome_codigo.descripcion
        item['ote_codigo'] = self.ote_codigo.codigo
        item['ote_descripcion'] = self.ote_codigo.descripcion
        item['codigo_NAE'] = self.getCodigoNae()
        item['codigo_NAE_descripcion'] = self.getDescripcionNae()
        item['org_codigo'] = self.getCodigoOrg()
        item['org_descripcion'] = self.getDescripcionOrg()
        item['osde_codigo'] = self.getCodigoOsde()
        item['osde_descripcion'] = self.getDescripcionOsde()
        return item

    def __str__(self):
        return "({0})-{1}".format(str(self.codigo_CI), self.nombre_CI)


