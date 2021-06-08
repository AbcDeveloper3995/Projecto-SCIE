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

class usuarioProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'username', 'password', 'email', 'image']
        exclude = [ 'user_permission', 'last_login', 'date_joined', 'is_staff', 'is_superuser', 'groups']
        widgets = {
            'first_name': TextInput(attrs={'class':'form-control'}),
            'last_name': TextInput(attrs={'class':'form-control'}),
            'username': TextInput(attrs={'class':'form-control'}),
            'password': PasswordInput(render_value=True, attrs={'class':'form-control'}),
            'email': EmailInput(attrs={'class':'form-control'}),
            'groups': SelectMultiple(attrs={'class':'form-control select2'}),
        }

class resetearPasswordForm(forms.Form):

    username = CharField(widget=TextInput(attrs={
        'placeholder':'Ingrese un usuario',
        'class':'form-control',
        'autocomplete': 'off'
    }))


    def clean(self):
        cleaned = super().clean()
        if not Usuario.objects.filter(username=cleaned['username']).exists():
            self._errors['error'] = self._errors.get('error', self.error_class())
            self._errors['error'].append('El usuario no existe')
        return cleaned

    def getUser(self):
        username = self.cleaned_data.get('username')
        return Usuario.objects.get(username=username)

class changePasswordForm(forms.Form):

    password = CharField(widget=PasswordInput(attrs={
        'placeholder':'Ingrese una contraseña',
        'class':'form-control',
        'autocomplete': 'off'
    }))

    confirmPassword = CharField(widget=PasswordInput(attrs={
        'placeholder': 'Repita su contraseña',
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    def clean(self):
        cleaned = super().clean()
        password = cleaned['password']
        confirmPassword = cleaned['confirmPassword']
        if password != confirmPassword:
            self._errors['error'] = self._errors.get('error', self.error_class())
            self._errors['error'].append('Las contraseñas no coinciden')
        return cleaned