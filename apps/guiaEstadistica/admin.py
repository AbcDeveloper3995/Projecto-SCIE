from django.contrib import admin
from django.contrib.auth.models import Permission

from apps.guiaEstadistica.models import *

admin.site.register(guiaEstadistica)
admin.site.register(cuestionario)
admin.site.register(universoEntidades)
admin.site.register(Permission)