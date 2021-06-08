from django.forms import *

from apps.guiaEstadistica.models import *


class guiaEstadisticaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = guiaEstadistica
        fields = '__all__'
        labels = {
                     'nombre': 'Nombre',
                     'activo': 'es_Activo'
        },
        widgets = {
            'nombre': TextInput(attrs={'class':'form-control', 'id':'guiaNombre', 'autofocus':'on'}),
            'activo': CheckboxInput(attrs={'class':'custom-control-input', 'type': 'checkbox', 'id':'guiaActiva'})
        }

class universoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(universoForm, self).__init__(*args, **kwargs)


    class Meta:
        model = universoEntidades
        fields = '__all__'
        widgets = {
            'guia': Select(attrs={'class':'form-control select2'}),
            'entidad_codigo': Select(attrs={'class':'form-control select2'}),
        }

    def clean(self):
        cleaned = super().clean()
        if universoEntidades.objects.filter(entidad_codigo=cleaned['entidad_codigo']).exists():
             self._errors['error'] = self._errors.get('error', self.error_class())
             self._errors['error'].append('Ese centro infomante ya forma parte del universo a evaluar.')
        return cleaned