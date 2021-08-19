from django.contrib import admin
from apps.indicadores.models import clasificadorIndicadores, posiblesRespuestas, Indicadores, PreguntasEvaluadas

admin.site.register(clasificadorIndicadores)
admin.site.register(posiblesRespuestas)
admin.site.register(Indicadores)
admin.site.register(PreguntasEvaluadas)
