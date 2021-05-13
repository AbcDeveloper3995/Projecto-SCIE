
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, CreateView, UpdateView

from SCIEv1 import settings
from apps.entidad.models import Entidad
from apps.guiaEstadistica.models import guiaEstadistica
from apps.usuario.form import usuarioForm, usuarioProfileForm
from apps.usuario.models import Usuario

# MOSTAR PAGINA PRINCIPAL
class homeView(LoginRequiredMixin, TemplateView):
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

# PROCEDIMIENTO PARA LOGIARSE.
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

# PROCEDIMIENTO PARA LISTAR USUARIOS.
class listarUsuariosView(LoginRequiredMixin, ListView):
    template_name = 'usuario/listarUsuario.html'
    model = Usuario
    context_object_name = 'usuarios'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Usuarios'
        return context

# PROCEDIMIENTO PARA CREAR USUARIOS.
class crearUsuarioView(LoginRequiredMixin, CreateView):
    template_name = 'usuario/crearUsuario.html'
    model = Usuario
    form_class = usuarioForm
    success_url = reverse_lazy('usuario:listarUsuario')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Creacion de usuario'
        return context

# PROCEDIMIENTO PARA MODIFICAR USUARIOS.
class updateUsuarioView(LoginRequiredMixin, UpdateView):
    model = Usuario
    form_class = usuarioForm
    template_name = 'usuario/crearUsuario.html'
    success_url = reverse_lazy('usuario:listarUsuario')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Edicion de usuario'
        return context

# PROCEDIMIENTO PARA ELIMINAR USUARIOS.
class eliminarUsuario(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        query = get_object_or_404(Usuario, id=self.kwargs['pk'])
        query.delete()
        messages.success(self.request, "El usuario " + query.first_name + " ha sido eliminado correctamente.")
        return redirect('usuario:listarUsuario')


# PROCEDIMIENTO PARA QUE UN USUARIO MODIFIQUE SU PERFIL.
class updateUsuarioProfileView(LoginRequiredMixin, UpdateView):
    model = Usuario
    form_class = usuarioProfileForm
    template_name = 'usuario/usuarioProfile.html'
    success_url = reverse_lazy('usuario:home')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Edicion de perfil'
        return context