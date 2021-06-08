from django.db import models


class organismo(models.Model):
    codigo = models.CharField(verbose_name='Codigo', max_length=5, primary_key=True,  blank=False, null=False)
    descripcion = models.CharField(verbose_name='Descripcion', max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'Organismo'
        verbose_name = 'COrganismo'
        verbose_name_plural = 'Organismo'
        ordering = ['codigo']

    def __str__(self):
        return str(self.codigo)

class osde(models.Model):
    codigo = models.CharField(verbose_name='Codigo', max_length=10, primary_key=True,  blank=False, null=False)
    descripcion = models.CharField(verbose_name='Descripcion', max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'OSDE'
        verbose_name = 'OSDE'
        verbose_name_plural = 'OSDE'
        ordering = ['codigo']

    def __str__(self):
        return str(self.codigo)


class clasificadorDPA(models.Model):
    codigo = models.IntegerField(verbose_name='Codigo', primary_key=True,  blank=False, null=False)
    descripcion = models.CharField(verbose_name='Descripcion', max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'Clasificador DPA'
        verbose_name = 'Clasificador_DPA'
        verbose_name_plural = 'Clasificador_DPA'
        ordering = ['codigo']

    def __str__(self):
        return str(self.codigo)


class clasificadorNAE(models.Model):
    codigo = models.CharField(verbose_name='Codigo', max_length=5, primary_key=True, blank=False, null=False)
    descripcion = models.CharField(verbose_name='Descripcion', max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'Clasificador NAE'
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

    def __str__(self):
        return "({0})-{1}".format(str(self.codigo_CI), self.nombre_CI)


