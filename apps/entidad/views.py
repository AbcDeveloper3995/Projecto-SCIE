from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, TemplateView

from apps.entidad.forms import entidadForm
from apps.entidad.models import *

# PROCEDIMIENTO PARA LISTAR LAS ENTIDADES
class listarEntidadView(ListView):
    model = Entidad
    template_name = 'entidad/listarEntidad.html'
    context_object_name = 'entidades'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Entidades'
        return context

# PROCEDIMIENTO PARA CREAR UNA ENTIDAD
class crearEntidadView(CreateView):
    template_name = 'entidad/crearEntidad.html'
    model = Entidad
    form_class = entidadForm
    success_url = reverse_lazy('entidad:listarEntidad')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Creacion de entidad'
        return context

# PROCEDIMIENTO PARA ACTUALIZAR UNA ENTIDAD
class updateEntidadView(UpdateView):
    model = Entidad
    form_class = entidadForm
    template_name = 'entidad/crearEntidad.html'
    success_url = reverse_lazy('entidad:listarEntidad')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Edicion de entidad'
        return context

# PROCEDIMIENTO PARA ELIMINAR UNA ENTIDAD
class eliminarEntidad(TemplateView):

    def get(self, request, *args, **kwargs):
        entidad = get_object_or_404(Entidad, id=self.kwargs['pk'])
        entidad.delete()
        messages.success(self.request, "La entidad " + entidad.nombre_CI + "ha sido eliminada correctamente.")
        return redirect('entidad:listarEntidad')
