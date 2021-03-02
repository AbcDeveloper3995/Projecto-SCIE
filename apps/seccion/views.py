from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, TemplateView, UpdateView

from apps.seccion.forms import *
from apps.seccion.models import *


class listarSeccionView(ListView):
    model = seccion
    template_name = 'seccion/listar/seccion.html'
    context_object_name = 'secciones'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Secciones'
        return context

class crearSeccionView(CreateView):
    model = seccion
    template_name = 'seccion/crear/seccion.html'
    form_class = seccionForm
    success_url = reverse_lazy('seccion:listarSeccion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Creacion de seccion'
        return context

class updateSeccionView(UpdateView):
    model = seccion
    form_class = seccionForm
    template_name = 'seccion/crear/seccion.html'
    success_url = reverse_lazy('seccion:listarSeccion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Edicion de seccion'
        return context

class eliminarSeccion(TemplateView):

    def get(self, request, *args, **kwargs):
        query = get_object_or_404(seccion, id=self.kwargs['pk'])
        query.delete()
        messages.success(self.request, "La seccion " + query.nombre + " de la guia " + query.guia_id.nombre + " ha sido eliminada correctamente.")
        return redirect('seccion:listarSeccion')

class listarPeriodoView(ListView):
    model = clasificadorPeriodo
    template_name = 'seccion/listar/periodo.html'
    context_object_name = 'periodos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Periodos'
        return context

class crearPeriodoView(CreateView):
    model = clasificadorPeriodo
    template_name = 'seccion/crear/periodo.html'
    form_class = periodoForm
    success_url = reverse_lazy('seccion:listarPeriodo')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Creacion de periodo'
        return context

class updatePeriodoView(UpdateView):
    model = clasificadorPeriodo
    form_class = periodoForm
    template_name = 'seccion/crear/periodo.html'
    success_url = reverse_lazy('seccion:listarPeriodo')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Edicion de periodo'
        return context

class eliminarPeriodo(TemplateView):

    def get(self, request, *args, **kwargs):
        query = get_object_or_404(clasificadorPeriodo, id=self.kwargs['pk'])
        query.delete()
        messages.success(self.request, "El periodo ha sido eliminado correctamente.")
        return redirect('seccion:listarPeriodo')

class listarCodigoView(ListView):
    model = nomencladorCodigo
    template_name = 'seccion/listar/codigo.html'
    context_object_name = 'codigos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Codigos'
        return context

class crearCodigoView(CreateView):
    model = nomencladorCodigo
    template_name = 'seccion/crear/codigo.html'
    form_class = codigoForm
    success_url = reverse_lazy('seccion:listarCodigo')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Creacion de codigo'
        return context

class updateCodigoView(UpdateView):
    model = nomencladorCodigo
    form_class = codigoForm
    template_name = 'seccion/crear/codigo.html'
    success_url = reverse_lazy('seccion:listarCodigo')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Edicion de codigo'
        return context

class eliminarCodigo(TemplateView):

    def get(self, request, *args, **kwargs):
        query = get_object_or_404(nomencladorCodigo, id=self.kwargs['pk'])
        query.delete()
        messages.success(self.request, "El codigo " + query.codigo + " ha sido eliminado correctamente.")
        return redirect('seccion:listarCodigo')

class listarColumnaView(ListView):
    model = nomencladorColumna
    template_name = 'seccion/listar/columna.html'
    context_object_name = 'columnas'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Columnas'
        return context

class crearColumnaView(CreateView):
    model = nomencladorColumna
    template_name = 'seccion/crear/columna.html'
    form_class = columnaForm
    success_url = reverse_lazy('seccion:listarColumna')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Creacion de columna'
        return context

class updateColumnaView(UpdateView):
    model = nomencladorColumna
    form_class = columnaForm
    template_name = 'seccion/crear/columna.html'
    success_url = reverse_lazy('seccion:listarColumna')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Edicion de columna'
        return context

class eliminarColumna(TemplateView):

    def get(self, request, *args, **kwargs):
        query = get_object_or_404(nomencladorColumna, id=self.kwargs['pk'])
        query.delete()
        messages.success(self.request, "La columna " + query.columna +  " ha sido eliminada correctamente.")
        return redirect('seccion:listarColumna')

class crearInstanciaView(TemplateView):
    template_name = 'guiaEstadistica/captarDatos.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        objSeccion = seccion.objects.get(id=request.POST['seccion_id'])
        try:
            if action == 'crearInstancia':
                if objSeccion.periodo_id.tipo == "Anual":
                    instancia = instanciaSeccion(
                        seccion_id_id=request.POST['seccion_id'],
                        codigo_id_id=request.POST['codigo_id'],
                        columna_id_id=request.POST['columna_id'],
                        registro_1=request.POST['registro_1'],
                        registro_2=None,
                        registro_3=None,
                        modelo_1=request.POST['modelo_1'],
                        modelo_2=None,
                        modelo_3=None,
                    )
                    instancia.save()
                else:
                    instancia = instanciaSeccion(
                        seccion_id_id=request.POST['seccion_id'],
                        codigo_id_id=request.POST['codigo_id'],
                        columna_id_id=request.POST['columna_id'],
                        registro_1=request.POST['registro_1'],
                        registro_2=request.POST['registro_2'],
                        registro_3=request.POST['registro_3'],
                        modelo_1=request.POST['modelo_1'],
                        modelo_2=request.POST['modelo_2'],
                        modelo_3=request.POST['modelo_3'],
                    )
                    instancia.save()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

class getColumnas(TemplateView):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'getColumnas':
                data = [{'id':'', 'text':'------'}]
                for i in nomencladorColumna.objects.filter(seccion_id=request.POST['id']):
                    data.append({'id':i.id, 'text':i.columna})
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

class getCodigos(TemplateView):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'getCodigos':
                data = [{'id':'', 'text':'------'}]
                columna = nomencladorColumna.objects.get(id=request.POST['id'])
                if columna.codigo_id.exists():
                    for i in columna.codigo_id.all():
                        data.append({'id':i.id, 'text':i.codigo})
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)


class comprobarIndicadoresEvaluados(TemplateView):
    template_name = 'guiaEstadistica/captardatos.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            print(request.POST['seccion'])
            obj_seccion = seccion.objects.get(id=request.POST['seccion'])
            obj_cuestionario = cuestionario.objects.last()
            obj_verificacion = verificacion(
                seccion_id=obj_seccion,
                cuestionario_fk=obj_cuestionario,
                indicadoresVerificados=request.POST['indicadoresVerificados'],
                indicadoresCoinciden=request.POST['indicadoresCoinciden'],
                indicadoresIncluidos=request.POST['indicadoresIncluidos'],
            )
            obj_verificacion.save()
            data['exito'] = 'Control y verificacion de la seccion ' + obj_seccion.nombre + ' realizadas conrrectamente.'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

class modificarInstanciasView(TemplateView):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        campos = dict(request.POST)
        try:
            if action == 'cargarInstancias':
                data = []
                query = instanciaSeccion.objects.filter(cuestionario_fk=request.POST['id'])
                for i in query:
                    data.append(i.toJSON())
            if action == 'modificarInstancias':
                id, modelo_1, modelo_2, modelo_3, registro_1, registro_2, registro_3 = [],[],[],[],[],[],[]
                for clave, valor in campos.items():
                    if clave == 'id':
                        id = valor
                    elif clave == 'modelo_1':
                        modelo_1 = valor
                    elif clave == 'modelo_2':
                        modelo_2 = valor
                    elif clave == 'modelo_3':
                        modelo_3 = valor
                    elif clave == 'registro_1':
                        registro_1 = valor
                    elif clave == 'registro_2':
                        registro_2 = valor
                    elif clave == 'registro_3':
                        registro_3 = valor

                i = 0
                while i < len(id):
                    aux = id[i], modelo_1[i], registro_1[i], modelo_2[i], registro_2[i], modelo_3[i], registro_3[i]
                    query =instanciaSeccion.objects.get(id=(aux[0]))
                    print(aux)
                    query.modelo_1=aux[1]
                    query.modelo_2=aux[3]
                    query.modelo_3=aux[5]
                    query.registro_1=aux[2]
                    query.registro_2=aux[4]
                    query.registro_3=aux[6]
                    query.save()
                    i += 1
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

