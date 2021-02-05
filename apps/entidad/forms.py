from django.forms import *

from apps.entidad.models import *


class entidadForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(entidadForm, self).__init__(*args, **kwargs)
        self.fields['ote_codigo'].queryset = clasificadorDPA.objects.filter(codigo__range=(21,41))
        self.fields['ome_codigo'].queryset = clasificadorDPA.objects.exclude(codigo__range=(21,41))
        self.fields['codigo_NAE'].queryset = clasificadorNAE.objects.all()
        self.fields['org_codigo'].queryset = organismo.objects.all()
        self.fields['osde_codigo'].queryset = osde.objects.all()


    class Meta:
        model = Entidad
        fields = '__all__'
        widgets = {
            'codigo_CI': TextInput(attrs={'class': 'form-control'}),
            'nombre_CI': TextInput(attrs={'class':'form-control'}),
            'ote_codigo': Select(attrs={'class':'form-control select2'}),
            'ome_codigo': Select(attrs={'class':'form-control select2'}),
            'codigo_NAE': Select(attrs={'class':'form-control select2'}),
            'org_codigo': Select(attrs={'class':'form-control select2 '}),
            'osde_codigo': Select(attrs={'class':'form-control select2'}),
 }


