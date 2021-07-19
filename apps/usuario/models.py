from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import model_to_dict

from SCIEv1.settings import MEDIA_URL, STATIC_URL


class Usuario(AbstractUser):
    image = models.ImageField(upload_to='user/%Y', blank=True, null=True)
    token = models.UUIDField(primary_key=False, editable=False, null=True, blank=True)
    fecha_creado = models.DateField(verbose_name='Fecha de creacion', auto_now=True)
    fecha_modificado = models.DateField(verbose_name='Fecha de modificacion', auto_now_add=True)

    class Meta:
        db_table = 'Usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['fecha_creado']


    def get_img(self):
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image)
        return '{}{}'.format(STATIC_URL, 'propios/img/empty.png')

    def toJSON(self):
        item = model_to_dict(self, exclude=['password', 'groups', 'user_permission'])
        if self.last_login:
            item['last_login'] = self.last_login.strftime('%d/%m/%Y')
        item['fecha_creado'] = self.fecha_creado.strftime('%d/%m/%Y')
        item['image'] = self.get_img()
        return item

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.set_password(self.password)
        else:
            query = Usuario.objects.get(pk=self.pk)
            if query.password != self.password:
                self.set_password(self.password)
        super().save(*args, **kwargs)


