import json

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, TemplateView, UpdateView

from apps.guiaEstadistica.forms import *
from apps.guiaEstadistica.models import guiaEstadistica
from apps.indicadores.forms import seccion, clasificadorIndicadores
from apps.indicadores.models import Indicadores
from apps.seccion.forms import nomencladorColumna, instanciaSeccion, instanciaForm, verificacionForm


class listarGuiasView(ListView):
    template_name = 'guiaEstadistica/listarGuia.html'
    model = guiaEstadistica
    context_object_name = 'guias'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Guias'
        return context

class crearGuiasView(CreateView):
    template_name = 'guiaEstadistica/crearGuia.html'
    model = guiaEstadistica
    form_class = guiaEstadisticaForm
    success_url = reverse_lazy('guia:listarGuias')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Creacion de guia'
        return context

class updateGuiaView(UpdateView):
    model = guiaEstadistica
    form_class = guiaEstadisticaForm
    template_name = 'guiaEstadistica/crearGuia.html'
    success_url = reverse_lazy('guia:listarGuias')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Edicion de guia'
        return context

class eliminarGuia(TemplateView):

    def get(self, request, *args, **kwargs):
        guia = get_object_or_404(guiaEstadistica, id=self.kwargs['pk'])
        guia.delete()
        messages.success(self.request,"La guia " + guia.nombre + " ha sido eliminada correctamente.")
        return redirect('guia:listarGuias')

class captarDatosView(TemplateView):
    template_name = 'guiaEstadistica/captarDatos.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        print(request.POST)
        action = request.POST['action']
        lastCuestionario = cuestionario.objects.last()
        query = instanciaSeccion.objects.filter(seccion_id=request.POST['id_seccion'], cuestionario_fk_id=lastCuestionario.id)
        try:
           if action == 'mostrarInstancias' and query.exists():
               data = []
               for i in query:
                    data.append(i.toJSON())
           else:
               data['error'] = 'error'
        except Exception as e:
            data['error'] =str(e)
        return JsonResponse(data, safe= False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['guia'] = self.getGuia()
        if context['guia'] == None:
            redirect('usuario:home')
        else:
            context['secciones'] = self.getSecciones()
            context['verificacionForm'] = verificacionForm
            context['columnas'] = self.getCol()
            context['instancias'] = self.getInstancias()
            context['instanciaForm'] = instanciaForm
            context['datos'] = self.getDatos()
            print(context['datos'])
            context['universo'] = self.getUniverso()
            context['titulo'] = 'Informacion vinculada a la entidad:'
        return context

    def getGuia(self):
        try:
            guia = guiaEstadistica.objects.get(activo=True)
            return guia
        except Exception as e:
            messages.error(self.request, "No hay guias activas en este momento.")
            return None


    def getSecciones(self):
        data = []
        guia = self.getGuia()
        secciones = seccion.objects.filter(guia_id=guia.id)
        for i in secciones:
            data.append(i.id)
        return data


    def getDatos(self):

        guia = self.getGuia()
        data = {}
        secciones = seccion.objects.filter(guia_id=guia.id)
        for i in secciones:
            data[i.nombre] = self.getGrupoIndicador(i.id)
            data.copy()
        return data

    def getGrupoIndicador(self, idSeccion):
        aux = []
        if clasificadorIndicadores.objects.filter(seccion_id=idSeccion).exists():
            grupoInd = clasificadorIndicadores.objects.filter(seccion_id=idSeccion)
            for i in grupoInd:
                aux.append(i)
                self.getIndicador(i, aux)
            return aux
        else:
            secciones = self.getSecciones()
            for i in secciones:
                if i == idSeccion:
                    query = seccion.objects.get(id=i)
                    aux.append(query)
            return aux

    def getIndicador(self, i, aux):
        indicadores = Indicadores.objects.filter(clasificadorIndicadores_id=i.id)
        for i in indicadores:
            aux.append(i)


    def getCol(self):
        data ={}
        secciones = self.getSecciones()
        for i in secciones:
            col = nomencladorColumna.objects.filter(seccion_id=i)
            data[i] = col
            data.copy()
        return data

    def getInstancias(self):
        data = {}
        secciones = self.getSecciones()
        for i in secciones:
            obj = instanciaSeccion.objects.filter(seccion_id=i)
            data[i] = obj
            data.copy()
        return data

    def getUniverso(self):
        data = []
        if self.request.user.is_superuser:
            dataUniverso = universoEntidades.objects.all()
            for i in dataUniverso:
                data.append(i.entidad_codigo)
        elif self.request.user.has_perm('guiaEstadistica.pinar'):
            dataUniverso = universoEntidades.objects.filter(guia__activo=True).filter(entidad_codigo__ote_codigo__codigo__exact=21)
            for i in dataUniverso:
                data.append(i.entidad_codigo)
        elif self.request.user.has_perm('guiaEstadistica.ver_entidades_artemisa'):
            dataUniverso = universoEntidades.objects.filter(guia__activo=True).filter(entidad_codigo__ote_codigo__codigo__exact=22)
            for i in dataUniverso:
                data.append(i.entidad_codigo)
        elif self.request.user.has_perm('guiaEstadistica.habana'):
            dataUniverso = universoEntidades.objects.filter(guia__activo=True).filter(entidad_codigo__ote_codigo__codigo__exact=23)
            for i in dataUniverso:
                data.append(i.entidad_codigo)
        elif self.request.user.has_perm('guiaEstadistica.ver_entidades_mayabeque'):
            dataUniverso = universoEntidades.objects.filter(guia__activo=True).filter(entidad_codigo__ote_codigo__codigo__exact=24)
            for i in dataUniverso:
                data.append(i.entidad_codigo)
        elif self.request.user.has_perm('guiaEstadistica.ver_entidades_matanzas'):
            dataUniverso = universoEntidades.objects.filter(guia__activo=True).filter(entidad_codigo__ote_codigo__codigo__exact=25)
            for i in dataUniverso:
                data.append(i.entidad_codigo)
        elif self.request.user.has_perm('guiaEstadistica.ver_entidades_villa_clara'):
            dataUniverso = universoEntidades.objects.filter(guia__activo=True).filter(entidad_codigo__ote_codigo__codigo__exact=26)
            for i in dataUniverso:
                data.append(i.entidad_codigo)
        elif self.request.user.has_perm('guiaEstadistica.ver_entidades_cienfuegos'):
            dataUniverso = universoEntidades.objects.filter(guia__activo=True).filter(entidad_codigo__ote_codigo__codigo__exact=27)
            for i in dataUniverso:
                data.append(i.entidad_codigo)
        elif self.request.user.has_perm('guiaEstadistica.ver_entidades_santi_spiritu'):
            dataUniverso = universoEntidades.objects.filter(guia__activo=True).filter(entidad_codigo__ote_codigo__codigo__exact=28)
            for i in dataUniverso:
                data.append(i.entidad_codigo)
        elif self.request.user.has_perm('guiaEstadistica.ver_entidades_ciego'):
            dataUniverso = universoEntidades.objects.filter(guia__activo=True).filter(entidad_codigo__ote_codigo__codigo__exact=29)
            for i in dataUniverso:
                data.append(i.entidad_codigo)
        elif self.request.user.has_perm('guiaEstadistica.ver_entidades_camaguey'):
            dataUniverso = universoEntidades.objects.filter(guia__activo=True).filter(entidad_codigo__ote_codigo__codigo__exact=30)
            for i in dataUniverso:
                data.append(i.entidad_codigo)
        elif self.request.user.has_perm('guiaEstadistica.ver_entidades_las_tunas'):
            dataUniverso = universoEntidades.objects.filter(guia__activo=True).filter(entidad_codigo__ote_codigo__codigo__exact=31)
            for i in dataUniverso:
                data.append(i.entidad_codigo)
        elif self.request.user.has_perm('guiaEstadistica.ver_entidades_holguin'):
            dataUniverso = universoEntidades.objects.filter(guia__activo=True).filter(entidad_codigo__ote_codigo__codigo__exact=32)
            for i in dataUniverso:
                data.append(i.entidad_codigo)
        elif self.request.user.has_perm('guiaEstadistica.ver_entidades_granma'):
            dataUniverso = universoEntidades.objects.filter(guia__activo=True).filter(entidad_codigo__ote_codigo__codigo__exact=33)
            for i in dataUniverso:
                data.append(i.entidad_codigo)
        elif self.request.user.has_perm('guiaEstadistica.ver_entidades_santiago'):
            dataUniverso = universoEntidades.objects.filter(guia__activo=True).filter(entidad_codigo__ote_codigo__codigo__exact=34)
            for i in dataUniverso:
                data.append(i.entidad_codigo)
        elif self.request.user.has_perm('guiaEstadistica.ver_entidades_guantanamo'):
            dataUniverso = universoEntidades.objects.filter(guia__activo=True).filter(entidad_codigo__ote_codigo__codigo__exact=35)
            for i in dataUniverso:
                data.append(i.entidad_codigo)
        elif self.request.user.has_perm('guiaEstadistica.ver_entidades_la_isla'):
            dataUniverso = universoEntidades.objects.filter(guia__activo=True).filter(entidad_codigo__ote_codigo__codigo__exact=40)
            for i in dataUniverso:
                data.append(i.entidad_codigo)
        elif self.request.user.has_perm('guiaEstadistica.ver_entidades_ZED_mariel'):
            dataUniverso = universoEntidades.objects.filter(guia__activo=True).filter(entidad_codigo__ote_codigo__codigo__exact=41)
            for i in dataUniverso:
                data.append(i.entidad_codigo)
        return data

class crearUniversoView(CreateView):
    template_name = 'entidad/crearUniverso.html'
    model = universoEntidades
    form_class = universoForm
    success_url = reverse_lazy('guia:listarUniverso')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Creacion de universo'
        return context

class updateUniversoView(UpdateView):
    model = universoEntidades
    form_class = universoForm
    template_name = 'entidad/crearUniverso.html'
    success_url = reverse_lazy('guia:listarUniverso')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Edicion de universo'
        return context


class listarUniversoView(ListView):
    model = universoEntidades
    template_name = 'entidad/listarUniverso.html'
    context_object_name = 'universo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Universos definidos'
        return context

class eliminarUniverso(TemplateView):

    def get(self, request, *args, **kwargs):
        universo = get_object_or_404(universoEntidades, id=self.kwargs['pk'])
        universo.delete()
        messages.success(self.request, "La entidad " + universo.entidad_codigo.nombre_CI + " ha sido eliminada del universo correctamente.")
        return redirect('guia:listarUniverso')

class dataUniversoView(TemplateView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        print(request.POST)
        dataJson = json.loads(request.POST['data'])
        enitdad = Entidad.objects.all()
        try:
            for j in enitdad:
                 for i in dataJson:
                     if i == j.codigo_CI:
                         print(i,j , 'Coinciden')
                         self.crearUniverso(j)
            data['exito'] = 'Universo creado correctamente.'
        except Exception as e:
            data['error'] =str(e)
        return JsonResponse(data, safe= False)


    def getGuia(self):
        guia = guiaEstadistica.objects.get(activo=True)
        return guia

    def crearUniverso(self, Entidad):
            obj = universoEntidades(
                guia=self.getGuia(),
                entidad_codigo=Entidad
            )
            obj.save()

class dataCaptacion(captarDatosView):
    template_name = 'guiaEstadistica/captarDatos.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        campos = dict(request.POST)
        action = campos.get('action')
        entidad = campos.get('Entidad')
        try:
            if action[0] == 'dataCaptacion':
                objCuestionario = self.createCuestionario(entidad)
                if objCuestionario == False:
                    data['error'] = 'La entidad seleccionada ya ha sido controlada.'
                else:
                    for clave, valor in campos.items():
                        if clave != 'action':
                            queryPreEval = PreguntasEvaluadas(
                                captacion_id=objCuestionario,
                                pregunta=clave,
                                respuesta=valor[0]
                            )
                            queryPreEval.save()
                    data['exito'] = 'Informacion guardada correctamente.'
            if action[0] == 'crearInstancia':
                objSeccion = seccion.objects.get(id=request.POST['seccion_id'])
                lastCuestionario = self.getLastCuestionario()
                if objSeccion.periodo_id.tipo == "Anual":
                    instancia = instanciaSeccion(
                        seccion_id_id=request.POST['seccion_id'],
                        cuestionario_fk=lastCuestionario,
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
                        cuestionario_fk=lastCuestionario,
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

    def createCuestionario(self, entidad):
        try:
            query = Entidad.objects.get(nombre_CI__exact=entidad[0])
            print(query)
            objCuestionario = cuestionario(
                    guia=self.getGuia(),
                    entidad_codigo=query
                )
            objCuestionario.save()
            return objCuestionario
        except:
            return False


    def getLastCuestionario(self):
        query = cuestionario.objects.last()
        return query


class guiaCaptada(ListView):
    template_name = 'guiaEstadistica/guiaCaptada.html'
    model = cuestionario
    context_object_name = 'cuestionarios'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_superuser:
            context['cuestionarios'] = cuestionario.objects.all()
        elif self.request.user.has_perm('guiaEstadistica.pinar'):
            context['cuestionarios'] = cuestionario.objects.filter(guia__activo=True).filter(
                entidad_codigo__ote_codigo__codigo__exact=21)
        elif self.request.user.has_perm('guiaEstadistica.ver_entidades_artemisa'):
            context['cuestionarios'] = cuestionario.objects.filter(guia__activo=True).filter(
                entidad_codigo__ote_codigo__codigo__exact=22)
        elif self.request.user.has_perm('guiaEstadistica.habana'):
            context['cuestionarios'] = cuestionario.objects.filter(guia__activo=True).filter(
                entidad_codigo__ote_codigo__codigo__exact=23)
        elif self.request.user.has_perm('guiaEstadistica.ver_entidades_mayabeque'):
            context['cuestionarios'] = cuestionario.objects.filter(guia__activo=True).filter(
                entidad_codigo__ote_codigo__codigo__exact=24)
        elif self.request.user.has_perm('guiaEstadistica.ver_entidades_matanzas'):
            context['cuestionarios'] = cuestionario.objects.filter(guia__activo=True).filter(
                entidad_codigo__ote_codigo__codigo__exact=25)
        elif self.request.user.has_perm('guiaEstadistica.ver_entidades_villa_clara'):
            context['cuestionarios'] = cuestionario.objects.filter(guia__activo=True).filter(
                entidad_codigo__ote_codigo__codigo__exact=26)
        elif self.request.user.has_perm('guiaEstadistica.ver_entidades_cienfuegos'):
            context['cuestionarios'] = cuestionario.objects.filter(guia__activo=True).filter(
                entidad_codigo__ote_codigo__codigo__exact=27)
        elif self.request.user.has_perm('guiaEstadistica.ver_entidades_santi_spiritu'):
            context['cuestionarios'] = cuestionario.objects.filter(guia__activo=True).filter(
                entidad_codigo__ote_codigo__codigo__exact=28)
        elif self.request.user.has_perm('guiaEstadistica.ver_entidades_ciego'):
            context['cuestionarios'] = cuestionario.objects.filter(guia__activo=True).filter(
                entidad_codigo__ote_codigo__codigo__exact=29)
        elif self.request.user.has_perm('guiaEstadistica.ver_entidades_camaguey'):
            context['cuestionarios'] = cuestionario.objects.filter(guia__activo=True).filter(
                entidad_codigo__ote_codigo__codigo__exact=30)
        elif self.request.user.has_perm('guiaEstadistica.ver_entidades_las_tunas'):
            context['cuestionarios'] = cuestionario.objects.filter(guia__activo=True).filter(
                entidad_codigo__ote_codigo__codigo__exact=31)
        elif self.request.user.has_perm('guiaEstadistica.ver_entidades_holguin'):
            context['cuestionarios'] = cuestionario.objects.filter(guia__activo=True).filter(
                entidad_codigo__ote_codigo__codigo__exact=32)
        elif self.request.user.has_perm('guiaEstadistica.ver_entidades_granma'):
            context['cuestionarios'] = cuestionario.objects.filter(guia__activo=True).filter(
                entidad_codigo__ote_codigo__codigo__exact=33)
        elif self.request.user.has_perm('guiaEstadistica.ver_entidades_santiago'):
            context['cuestionarios'] = cuestionario.objects.filter(guia__activo=True).filter(
                entidad_codigo__ote_codigo__codigo__exact=34)
        elif self.request.user.has_perm('guiaEstadistica.ver_entidades_guantanamo'):
            context['cuestionarios'] = cuestionario.objects.filter(guia__activo=True).filter(
                entidad_codigo__ote_codigo__codigo__exact=35)
        elif self.request.user.has_perm('guiaEstadistica.ver_entidades_la_isla'):
            context['cuestionarios'] = cuestionario.objects.filter(guia__activo=True).filter(
                entidad_codigo__ote_codigo__codigo__exact=40)
        elif self.request.user.has_perm('guiaEstadistica.ver_entidades_ZED_mariel'):
            context['cuestionarios'] = cuestionario.objects.filter(guia__activo=True).filter(
                entidad_codigo__ote_codigo__codigo__exact=41)
        context['titulo'] = 'Cuestionarios captados'
        context['titulo2'] = 'Informacion Captada'
        context['titulo3'] = 'Modificar Preguntas'
        context['titulo4'] = 'Modificar Instancias'
        return context

class eliminarGuiaCaptada(TemplateView):

    def get(self, request, *args, **kwargs):
        guia = get_object_or_404(cuestionario, id=self.kwargs['pk'])
        guia.delete()
        messages.success(self.request,"el cuestionario captado a " + guia.entidad_codigo.nombre_CI + " ha sido eliminado correctamente.")
        return redirect('guia:guiaCaptada')

class informacionCaptada(TemplateView):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'informacionCaptada':
                data = []
                preguntasCaptadas = PreguntasEvaluadas.objects.filter(captacion_id=request.POST['id'])
                for i in preguntasCaptadas:
                    data.append(i.toJSON())
                instancias = instanciaSeccion.objects.filter(cuestionario_fk=request.POST['id'])
                for i in instancias:
                    data.append(i.toJSON())
            else:
                pass
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)


class seccionCaptada(TemplateView):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'seccionCaptada':
                data = []
                query_seccion = seccion.objects.get(id=request.POST['id'])
                if query_seccion.periodo_id =='Anual':
                    instancia = instanciaSeccion.objects.filter(seccion_id_id=query_seccion.id)
                    for i in instancia:
                        data.append(i.toJSON())
                else:
                    instancia = instanciaSeccion.objects.filter(seccion_id_id=query_seccion.id)
                    for i in instancia:
                        data.append(i.toJSON())
            else:
                pass
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)



class modificarPreguntasView(TemplateView):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        campos = dict(request.POST)
        print(campos)
        try:
            if action == 'cargarPreguntas':
               data = []
               query = PreguntasEvaluadas.objects.filter(captacion_id=request.POST['id'])
               for i in query:
                   data.append(i.toJSON())
            if action == 'modificarPreguntas':
                for clave, valor in campos.items():
                    if clave != 'action' and clave != 'id':
                        query = PreguntasEvaluadas.objects.filter(pregunta=clave).filter(captacion_id=campos['id'][0])
                        pregunta = query[0]
                        pregunta.respuesta = valor[0]
                        pregunta.save()

        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
