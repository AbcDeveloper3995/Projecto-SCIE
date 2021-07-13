from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, TemplateView

from apps.entidad.forms import entidadForm
from apps.entidad.models import *

# PROCEDIMIENTO PARA LISTAR LAS ENTIDADES
class listarEntidadView(LoginRequiredMixin, TemplateView):
    template_name = 'entidad/listarEntidad.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'getEntidades':
                query = Entidad.objects.all()
                data = []
                for i in query:
                    data.append(i.toJSON())
            else:
                data['error'] = 'error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Entidades'
        return context

# PROCEDIMIENTO PARA CREAR UNA ENTIDAD
class crearEntidadView(LoginRequiredMixin, CreateView):
    template_name = 'entidad/crearEntidad.html'
    model = Entidad
    form_class = entidadForm
    success_url = reverse_lazy('entidad:listarEntidad')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Creacion de entidad'
        return context

# PROCEDIMIENTO PARA ACTUALIZAR UNA ENTIDAD
class updateEntidadView(LoginRequiredMixin, UpdateView):
    model = Entidad
    form_class = entidadForm
    template_name = 'entidad/crearEntidad.html'
    success_url = reverse_lazy('entidad:listarEntidad')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Edicion de entidad'
        return context

# PROCEDIMIENTO PARA ELIMINAR UNA ENTIDAD
class eliminarEntidad(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        entidad = get_object_or_404(Entidad, id=self.kwargs['pk'])
        entidad.delete()
        messages.success(self.request, "La entidad " + entidad.nombre_CI + " ha sido eliminada correctamente.")
        return redirect('entidad:listarEntidad')
