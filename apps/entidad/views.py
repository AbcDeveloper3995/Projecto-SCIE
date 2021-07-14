from tablib import Dataset
import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, TemplateView

from apps.entidad.admin import EntidadResource
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

# PROCEDIMIENTO PARA ELIMINAR TODAS LAS ENTIDADES SELECCIONADAS
class eliminarCIselectedView(LoginRequiredMixin, TemplateView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        listaEnitdadesSelected = json.loads(request.POST['data'])
        try:
            if action == 'eliminarCIselected':
                for i in listaEnitdadesSelected:
                    query = Entidad.objects.get(id=i['id'])
                    query.delete()
                data['exito'] = 'Las entidades seleccionadas se han eliminado correctamente.'
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] =str(e)
        return JsonResponse(data, safe=False)

# PROCEDIMIENTO PARA IMPORTAR  ENTIDAD
class importarEntidad(LoginRequiredMixin, TemplateView):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        file = request.FILES['datosCI']
        dataset = Dataset()
        try:
            if not file.name.endswith('xlsx'):
                data['error'] = 'El formato del documento no es valido.'
            else:
                entidadImportada = dataset.load(file.read(), format='xlsx')
                for i in entidadImportada:
                    entidad = Entidad(
                        i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7],
                    )
                    entidad.save()
                data['exito'] = 'Las nuevas entidades se han creado correctamente.'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)


# PROCEDIMIENTO PARA IMPORTAR  OSDE
class importarOSDE(LoginRequiredMixin, TemplateView):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        file = request.FILES['datosOSDE']
        dataset = Dataset()
        try:
            if not file.name.endswith('xlsx'):
                data['error'] = 'El formato del documento no es valido.'
            else:
                osdeImportado = dataset.load(file.read(), format='xlsx')
                for i in osdeImportado:
                    objOSDE = osde(
                        i[0], i[1], i[2]
                    )
                    objOSDE.save()
                data['exito'] = 'Los nuevos OSDE se han creado correctamente.'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)


# PROCEDIMIENTO PARA IMPORTAR  NAE
class importarNAE(LoginRequiredMixin, TemplateView):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        file = request.FILES['datosNAE']
        dataset = Dataset()
        try:
            if not file.name.endswith('xlsx'):
                data['error'] = 'El formato del documento no es valido.'
            else:
                naeImportado = dataset.load(file.read(), format='xlsx')
                for i in naeImportado:
                    nae = clasificadorNAE(
                        i[0], i[1], i[2]
                    )
                    nae.save()
                data['exito'] = 'Los nuevos NAE se han creado correctamente.'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)


# PROCEDIMIENTO PARA IMPORTAR  ORGANISMO
class importarOrganismo(LoginRequiredMixin, TemplateView):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        file = request.FILES['datosOrganismo']
        dataset = Dataset()
        try:
            if not file.name.endswith('xlsx'):
                data['error'] = 'El formato del documento no es valido.'
            else:
                orgImportado = dataset.load(file.read(), format='xlsx')
                for i in orgImportado:
                    objOrganismo = organismo(
                        i[0], i[1], i[2]
                    )
                    organismo.save()
                data['exito'] = 'Las nuevas entidades se han creado correctamente.'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)