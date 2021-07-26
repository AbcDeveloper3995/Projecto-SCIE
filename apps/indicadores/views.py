from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, TemplateView

from apps.indicadores.forms import *
from apps.indicadores.models import *

# PROCEDIMIENTO PARA LISTAR GRUPO DE PREGUNTAS.
class listarClasificadIndicadorView(LoginRequiredMixin, ListView):
    template_name = 'indicadores/listar/grupoPreguntas.html'
    model = clasificadorIndicadores
    context_object_name = 'clasificadorInds'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Grupo de Preguntas'
        context['tituloPestaña'] = 'SCIE | Grupo-Preguntas'
        return context

# PROCEDIMIENTO PARA CREAR GRUPO DE PREGUNTAS.
class crearClasificadorIndicadorView(LoginRequiredMixin, CreateView):
    template_name = 'indicadores/crear/grupoPreguntas.html'
    model = clasificadorIndicadores
    form_class = clasificadorIndicadorForm
    success_url = reverse_lazy('indicador:istarClasificador')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Creacion de grupo de preguntas'
        context['tituloPestaña'] = 'SCIE | Grupo-Preguntas'
        return context

# PROCEDIMIENTO PARA MODIFICAR GRUPO DE PREGUNTAS.
class updateClasificadorIndView(LoginRequiredMixin, UpdateView):
    model = clasificadorIndicadores
    form_class = clasificadorIndicadorForm
    template_name = 'indicadores/crear/grupoPreguntas.html'
    success_url = reverse_lazy('indicador:istarClasificador')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Edicion de grupo de preguntas'
        context['tituloPestaña'] = 'SCIE | Grupo-Preguntas'
        return context

# PROCEDIMIENTO PARA ELIMINAR GRUPO DE PREGUNTAS.
class eliminarClasificadorInd(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        query = get_object_or_404(clasificadorIndicadores, id=self.kwargs['pk'])
        query.delete()
        messages.success(self.request, "El grupo de preguntas " + query.nombre + " ha sido eliminado correctamente.")
        return redirect('indicador:istarClasificador')

# PROCEDIMIENTO PARA LISTAR PREGUNTAS.
class listarIndicadorView(LoginRequiredMixin, ListView):
    template_name = 'indicadores/listar/preguntas.html'
    model = Indicadores
    context_object_name = 'indicadores'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Preguntas'
        context['tituloPestaña'] = 'SCIE | Preguntas'
        return context

# PROCEDIMIENTO PARA CREAR PREGUNTAS.
class crearIndicadorView(LoginRequiredMixin, CreateView):
    template_name = 'indicadores/crear/preguntas.html'
    model = clasificadorIndicadores
    form_class = indicadorForm
    success_url = reverse_lazy('indicador:listarIndicador')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Creacion de preguntas'
        context['tituloPestaña'] = 'SCIE | Preguntas'
        return context

# PROCEDIMIENTO PARA MODIFICAR PREGUNTAS.
class updateIndicadorView(LoginRequiredMixin, UpdateView):
    model = Indicadores
    form_class = indicadorForm
    template_name = 'indicadores/crear/preguntas.html'
    success_url = reverse_lazy('indicador:listarIndicador')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Edicion de preguntas'
        context['tituloPestaña'] = 'SCIE | Preguntas'
        return context

# PROCEDIMIENTO PARA ELIMINAR PREGUNTAS.
class eliminarIndicador(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        query = get_object_or_404(Indicadores, id=self.kwargs['pk'])
        query.delete()
        messages.success(self.request, "La pregunta " + query.nombre + " ha sido eliminada correctamente.")
        return redirect('indicador:listarIndicador')

# PROCEDIMIENTO PARA LISTAR RESPUESTAS.
class listarPosiblesRespuestasView(LoginRequiredMixin, ListView):
    template_name = 'indicadores/listar/posiblesResp.html'
    model = posiblesRespuestas
    context_object_name = 'posiblesRespuestas'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Posibles Respuestas'
        context['tituloPestaña'] = 'SCIE | Respuestas'
        return context

# PROCEDIMIENTO PARA CREAR RESPUESTAS.
class crearPosiblesRespuestasView(LoginRequiredMixin, CreateView):
    template_name = 'indicadores/crear/posiblesResp.html'
    model = posiblesRespuestas
    form_class = posiblesRespuestasForm
    success_url = reverse_lazy('indicador:listarRespuesta')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Creacion de posibles respuestas'
        context['tituloPestaña'] = 'SCIE | Respuestas'
        return context

# PROCEDIMIENTO PARA MODIFICAR RESPUESTAS.
class updatePosiblresResView(LoginRequiredMixin, UpdateView):
    model = posiblesRespuestas
    form_class = posiblesRespuestasForm
    template_name = 'indicadores/crear/posiblesResp.html'
    success_url = reverse_lazy('indicador:listarRespuesta')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Edicion de respuestas'
        context['tituloPestaña'] = 'SCIE | Respuestas'
        return context

# PROCEDIMIENTO PARA ELIMINAR RESPUESTAS.
class eliminarPosibleRes(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        query = get_object_or_404(posiblesRespuestas, id=self.kwargs['pk'])
        query.delete()
        messages.success(self.request, "La respuesta " + query.nombre + " ha sido eliminada correctamente.")
        return redirect('indicador:listarRespuesta')