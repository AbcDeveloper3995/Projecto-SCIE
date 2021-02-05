from django.forms import *

from apps.indicadores.models import *




class clasificadorIndicadorForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['seccion_id'].queryset = seccion.objects.all()

    class Meta:
        model = clasificadorIndicadores
        fields = '__all__'
        widgets = {
            'seccion_id': Select(attrs={'class':'form-control select2'}),
            'nombre': TextInput(attrs={'class':'form-control'}),
            'activo': CheckboxInput(attrs={'class':'custom-control-input', 'type': 'checkbox', 'id':'clasificadorIndActiva' })
        }


class indicadorForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['clasificadorIndicadores_id'].queryset = clasificadorIndicadores.objects.all()

    class Meta:
        model = Indicadores
        fields = '__all__'
        labels = {
                     'nombre': 'Nombre',
                     'respuestas': 'Respuesta',
                     'clasificadorIndicadores': 'Clasificador al que se asocia',
                     'activo': 'es_Activo'
                 },
        widgets = {
            'nombre': TextInput(attrs={'class':'form-control'}),
            'cod_indicador': NumberInput(attrs={'class':'form-control'}),
            'respuestas_id': SelectMultiple(attrs={'class':'form-control select2'}),
            'clasificadorIndicadores_id': Select(attrs={'class':'form-control select2'}),
            'activo': CheckboxInput(attrs={'class':'custom-control-input', 'type': 'checkbox', 'id':'indicadorActiva' })
        }

class posiblesRespuestasForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = posiblesRespuestas
        fields = '__all__'
        labels = {
                     'nombre': 'Nombre',
                     'tipo_dato': 'Tipo de Dato',
                     'activo': 'es_Activo'
                 },
        widgets = {
            'nombre': TextInput(attrs={'class':'form-control'}),
            'tipo_dato': Select(attrs={'class':'form-control select2'}),
            'activo': CheckboxInput(attrs={'class':'custom-control-input', 'type': 'checkbox', 'id':'prActiva' })
        }