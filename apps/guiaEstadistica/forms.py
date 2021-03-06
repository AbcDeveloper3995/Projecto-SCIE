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
            'nombre': TextInput(attrs={'class':'form-control'}),
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