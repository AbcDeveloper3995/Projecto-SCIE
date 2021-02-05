from django.forms import *

from apps.seccion.models import *

CHOICES_INDICADOR = (
    ('', '------'),
    ('Si', 'Si'),
    ('No', 'No')
)


class seccionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['guia_id'].queryset = guiaEstadistica.objects.all()
        self.fields['periodo_id'].queryset = clasificadorPeriodo.objects.all()

    class Meta:
        model = seccion
        fields = '__all__'
        widgets = {
            'nombre': TextInput(attrs={'class':'form-control'}),
            'guia_id': Select(attrs={'class':'form-control select2'}),
            'periodo_id': Select(attrs={'class':'form-control select2'}),
            'numero': TextInput(attrs={'class':'form-control'}),
            'subNumero': TextInput(attrs={'class':'form-control'}),
            'orden': NumberInput(attrs={'class':'form-control '}),
            'tipo': Select(attrs={'class':'form-control select2'}),
            'activo': CheckboxInput(attrs={'class':'custom-control-input', 'type': 'checkbox', 'id':'seccionActiva' })
        }


class periodoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = clasificadorPeriodo
        fields = '__all__'
        labels = {
                     'tipo': 'Tipo de periodo',
                     'mes_1': 'Mes No.1',
                     'mes_2': 'Mes No.2',
                     'mes_3': 'Mes No.3',
                     'ano': 'Año'
                 },
        widgets = {
            'tipo': Select(attrs={'class':'form-control select2'}),
            'mes_1': Select(attrs={'class':'form-control select2'}),
            'mes_2': Select(attrs={'class':'form-control select2 '}),
            'mes_3': Select(attrs={'class':'form-control select2'}),
            'ano_1': Select(attrs={'class':'form-control select2'}),
            'ano_2': Select(attrs={'class':'form-control select2'}),
        }

class codigoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = nomencladorCodigo
        fields = '__all__'
        labels = {
                     'codigo': 'Codigo',
                     'descripcion': 'Descripcion',
                     'activo': 'Es activo',
                     'seccion_id': 'Seccion al que pertenece'
                 },
        widgets = {
            'codigo': TextInput(attrs={'class':'form-control'}),
            'descripcion': TextInput(attrs={'class':'form-control '}),
            'activo': CheckboxInput(attrs={'class':'custom-control-input', 'type': 'checkbox','id':'codigoActiva' }),
            'seccion_id': Select(attrs={'class':'form-control select2'})
        }

class columnaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['codigo_id'].queryset = nomencladorCodigo.objects.all()
        self.fields['seccion_id'].queryset = seccion.objects.all().exclude(nombre='Identificacion').exclude(nombre='Sobre_Entidad')

    class Meta:
        model = nomencladorColumna
        fields = '__all__'
        widgets = {
            'seccion_id': Select(attrs={'class':'form-control select2', 'style':'width:100%'}),
            'columna': TextInput(attrs={'class':'form-control '}),
            'descripcion': TextInput(attrs={'class':'form-control'}),
            'activo': CheckboxInput(attrs={'class':'custom-control-input', 'type': 'checkbox', 'id':'columnaActiva'}),
            'codigo_id': SelectMultiple(attrs={'class':'form-control select2', 'style':'width:100%'})
        }


class instanciaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['seccion_id'].queryset = seccion.objects.filter(guia_id__activo=True).exclude(nombre='Identificacion').exclude(nombre='Sobre_Entidad')
        self.fields['codigo_id'].queryset = nomencladorCodigo.objects.none()
        self.fields['columna_id'].queryset = nomencladorColumna.objects.none()
    class Meta:
        model = instanciaSeccion
        fields = '__all__'
        widgets = {
            'seccion_id': Select(attrs={'class':'form-control col-12 select2', 'name':'seccion_id'}),
            'codigo_id': Select(attrs={'class':'form-control col-12', 'name':'codigo_id'}),
            'columna_id': Select(attrs={'class':'form-control col-12','name':'columna_id'}),
            'registro_1':  NumberInput(attrs={'class':'form-control col-12'}),
            'modelo_1':  NumberInput(attrs={'class':'form-control col-12'}),
            'registro_2':  NumberInput(attrs={'class':'form-control col-12'}),
            'modelo_2': NumberInput(attrs={'class':'form-control col-12'}),
            'registro_3':  NumberInput(attrs={'class':'form-control col-12'}),
            'modelo_3':  NumberInput(attrs={'class':'form-control col-12'}),
        }

class verificacionForm(Form):
    indicadoresVerificados = CharField(label='Cantidad de indicadores verificados', widget=NumberInput(attrs={
        'class': 'form-control ',
        'placeholder': 'Ingrese un numero'
    }))
    indicadoresCoinciden = CharField(label='Cantidad de indicadores coincides', widget=NumberInput(attrs={
        'class': 'form-control ',
        'placeholder': 'Ingrese un numero'
    }))
    indicadoresIncluidos = ChoiceField(label='Estan incluidos en la informacion todos los establecimientos ?',
                                       widget=Select(attrs={'class':'form-control'}), choices=CHOICES_INDICADOR)