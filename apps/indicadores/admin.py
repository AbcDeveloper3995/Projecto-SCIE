from django.contrib import admin
from apps.indicadores.models import clasificadorIndicadores, posiblesRespuestas, Indicadores

admin.site.register(clasificadorIndicadores)
admin.site.register(posiblesRespuestas)
admin.site.register(Indicadores)
