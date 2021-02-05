import pyttsx3

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, CreateView, UpdateView

from SCIEv1 import settings
from apps.entidad.models import Entidad
from apps.guiaEstadistica.models import guiaEstadistica
from apps.usuario.form import usuarioForm
from apps.usuario.models import Usuario

def voz(request):
    eng = pyttsx3.init()
    list_voices = eng.getProperty("voices")
    eng.setProperty("voice", list_voices[0].id)
    eng.setProperty("rate", 130)
    eng.setProperty('volumen', 1.0)
    eng.say('Bienvenido, ingrese sus credenciales para acceder al Sistema de Control Integral Estatal.')
    eng.runAndWait()




class homeView(TemplateView):
    template_name = 'comun/home.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['guias'] = guiaEstadistica.objects.all().count()
        context['entidades'] = Entidad.objects.all().count()
        context['usuarios'] = Usuario.objects.all().count()
        return context


class Login(LoginView):
    template_name = 'usuario/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Inicio de sesion'
        return context

class listarUsuariosView(ListView):
    template_name = 'usuario/listarUsuario.html'
    model = Usuario
    context_object_name = 'usuarios'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Usuarios'
        return context

class crearUsuarioView(CreateView):
    template_name = 'usuario/crearUsuario.html'
    model = Usuario
    form_class = usuarioForm
    success_url = reverse_lazy('usuario:listarUsuario')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Creacion de usuario'
        return context


class updateUsuarioView(UpdateView):
    model = Usuario
    form_class = usuarioForm
    template_name = 'usuario/crearUsuario.html'
    success_url = reverse_lazy('usuario:listarUsuario')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Edicion de usuario'
        return context

class eliminarUsuario(TemplateView):

    def get(self, request, *args, **kwargs):
        query = get_object_or_404(Usuario, id=self.kwargs['pk'])
        query.delete()
        messages.success(self.request, "El usuario " + query.first_name + " ha sido eliminado correctamente.")
        return redirect('usuario:listarUsuario')