
import smtplib
import uuid
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView
from django.views.generic import TemplateView, ListView, CreateView, UpdateView

import SCIEv1.settings as setting

from apps.entidad.models import Entidad
from apps.guiaEstadistica.models import guiaEstadistica
from apps.usuario.form import resetearPasswordForm, changePasswordForm
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
            return redirect(setting.LOGIN_REDIRECT_URL)
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

#PROCEDIMIENTO PARA RESETEAR LA CONTRASEÑA POR CORREO
class resetearPasswordView(FormView):
    form_class = resetearPasswordForm
    template_name = 'usuario/resetearPassword.html'
    success_url = reverse_lazy(setting.LOGIN_REDIRECT_URL)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = resetearPasswordForm(request.POST)
            if form.is_valid():
                user = form.getUser()
                data = self.sendEmail(user)
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def sendEmail(self, user):
        data = {}
        try:

            URL = setting.DOMAIN if not setting.DEBUG else self.request.META['HTTP_HOST']
            #TOKEN PARA CREAR UNA URL SEGURA MEDIANTE UN CODIGO ALEATORIO
            user.token = uuid.uuid4()
            user.save()

            emailServidor = smtplib.SMTP(setting.EMAIL_HOST, setting.EMAIL_PORT)
            emailServidor.starttls()
            emailServidor.login(setting.EMAIL_HOST_USER, setting.EMAIL_HOST_PASSWORD)

            email = user.email
            sms = MIMEMultipart()
            sms['From'] = setting.EMAIL_HOST_USER
            sms['To'] = email
            sms['Subject'] = 'Reseteo de contraseña'

            content = render_to_string('usuario/enviarEmail.html',{
                'user': user.first_name,
                'link_resetpwd': 'http://{}/change/password/{}/'.format(URL, str(user.token)),
                'link_home': 'http://{}'.format(URL)
            })
            sms.attach(MIMEText(content,'html'))
            emailServidor.sendmail(setting.EMAIL_HOST_USER, email, sms.as_string())
        except Exception as e:
            data['error'] = str(e)
        return data

#PROCEDIMIENTO PARA EFECTUAR EL CAMBIO DE CONTRASEÑA UNA VEZ RESIVIDO EL CORREO
class changePasswordView(FormView):
    form_class = changePasswordForm
    template_name = 'usuario/changePaswsword.html'
    success_url = reverse_lazy(setting.LOGIN_REDIRECT_URL)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        token = self.kwargs['token']
        if Usuario.objects.filter(token=token).exists():
            return super().get(request, *args, **kwargs)
        return HttpResponseRedirect('/')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = changePasswordForm(request.POST)
            if form.is_valid():
                user = Usuario.objects.get(token=self.kwargs['token'])
                user.password = request.POST['password']
                #user.set_password(request.POST['password'])
                user.token = uuid.uuid4()
                user.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reseteo de Contraseña'
        context['login_url'] = setting.LOGIN_URL
        return context
