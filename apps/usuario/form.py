from django.forms import *

from apps.usuario.models import *


class usuarioForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'username', 'password', 'email', 'image', 'groups']
        exclude = [ 'user_permission', 'last_login', 'date_joined', 'is_staff', 'is_superuser']
        widgets = {
            'first_name': TextInput(attrs={'class':'form-control'}),
            'last_name': TextInput(attrs={'class':'form-control'}),
            'username': TextInput(attrs={'class':'form-control'}),
            'password': PasswordInput(render_value=True, attrs={'class':'form-control'}),
            'email': EmailInput(attrs={'class':'form-control'}),
            'groups': SelectMultiple(attrs={'class':'form-control select2'}),
        }