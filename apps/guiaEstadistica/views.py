import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, TemplateView, UpdateView

from apps.guiaEstadistica.forms import *
from apps.guiaEstadistica.models import guiaEstadistica, cuestionario
from apps.indicadores.forms import seccion, clasificadorIndicadores
from apps.indicadores.models import Indicadores, PreguntasEvaluadas
from apps.seccion.forms import nomencladorColumna, instanciaSeccion, instanciaForm, verificacionForm
from apps.seccion.models import clasificadorPeriodo
from utils import getCuestionarios, getUniverso


# PROCEDIMIENTO PARA LISTAR LAS GUIAS.
class listarGuiasView(LoginRequiredMixin, ListView):
    template_name = 'guiaEstadistica/listarGuia.html'
    model = guiaEstadistica
    context_object_name = 'guias'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Guias'
        context['tituloPestaña'] = 'SCIE | Guia'
        return context

# PROCEDIMIENTO PARA CREAR UNA GUIA.
class crearGuiasView(LoginRequiredMixin, CreateView):
    template_name = 'guiaEstadistica/crearGuia.html'
    model = guiaEstadistica
    form_class = guiaEstadisticaForm
    success_url = reverse_lazy('guia:listarGuias')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Creacion de guia'
        context['action'] = 'add'
        context['tituloPestaña'] = 'SCIE | Guia'
        context['guias'] = self.getGuias()
        return context

    def getGuias(self):
        query = guiaEstadistica.objects.all()
        return query

# PROCEDIMIENTO PARA ACTUALIZAR UNA GUIA.
class updateGuiaView(LoginRequiredMixin, UpdateView):
    model = guiaEstadistica
    form_class = guiaEstadisticaForm
    template_name = 'guiaEstadistica/crearGuia.html'
    success_url = reverse_lazy('guia:listarGuias')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Edicion de guia'
        context['tituloPestaña'] = 'SCIE | Guia'
        return context

# PROCEDIMIENTO PARA ELIMINAR UNA GUIA.
class eliminarGuia(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        guia = get_object_or_404(guiaEstadistica, id=self.kwargs['pk'])
        guia.delete()
        messages.success(self.request,"La guia " + guia.nombre + " ha sido eliminada correctamente.")
        return redirect('guia:listarGuias')

# PROCEDIMIENTO PARA OBTENER Y MOSTRAR TODA LA CONFIGURACION DE UNA GUIA, PARA PODER CAPTAR LOS DATOS NECESARIOS.
class captarDatosView(LoginRequiredMixin, TemplateView):
    template_name = 'guiaEstadistica/captardatos.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        idCuestionario = int(request.POST['id_cuestionario'])
        '''OBTENER EL ULTIMO CUESTIONARIO CREADO, EL CUAL ES CREADO AUTOMATICAMENTE CUANDO SE SALVA LO CAPTADO 
           EN LA SECCION IDENTIFICACION Y SOBRE ENTIDAD'''
        lastCuestionario = cuestionario.objects.last()
        try:
            '''LAS CONDICION == 0 ES PARA CUANDO SE ESTA CAPTANDO INSTANCIAS NUEVAS DESDE UN INICIO 
            DE LAS SECCIONES Y LA OTRA ES PARA CONTINUAR CON LA CAPTACION DE INSTANCIA DE UN CUESTIONARIO DE 
            UN CI YA CAPTADO'''
            if idCuestionario == 0:
                 query = instanciaSeccion.objects.filter(seccion_id=request.POST['id_seccion'], cuestionario_fk_id=lastCuestionario.id)
            else:
                query = instanciaSeccion.objects.filter(seccion_id=request.POST['id_seccion'],
                                                        cuestionario_fk_id=idCuestionario)
            if action == 'mostrarInstancias' and query.exists():
                data = []
                for i in query:
                    data.append(i.toJSON())
            else:
                data['codigo_id'] = '0'
                data['columna_id'] = '0'
                data['registro_1'] = '0'
                data['modelo_1'] = '0'
                data['diferencia_1'] = '0'
                data['registro_2'] = '0'
                data['modelo_2'] = '0'
                data['diferencia_2'] = '0'
                data['registro_3'] = '0'
                data['modelo_3'] = '0'
                data['diferencia_3'] = '0'
        except Exception as e:
            data['error'] =str(e)
        return JsonResponse(data, safe= False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['guia'] = self.getGuia()
        if context['guia'] == None:
            redirect('usuario:home')
        else:
            context['action'] = 'add'
            context['tituloPestaña'] = 'SCIE | Guia'
            context['secciones'] = self.getSecciones()
            context['verificacionForm'] = verificacionForm
            context['columnas'] = self.getCol()
            context['instancias'] = self.getInstancias()
            context['instanciaForm'] = instanciaForm
            context['datos'] = self.getDatos()
            context['universo'] = getUniverso(self.request.user)
        return context

    # FUNCION PARA OBTENER LA GUIA ACTIVA
    def getGuia(self):
        try:
            guia = guiaEstadistica.objects.get(activo=True)
            return guia
        except Exception as e:
            messages.error(self.request, "No hay guias activas en este momento.")
            return None

    # FUNCION PARA OBTENER LAS SECCIONES DE LA GUIA ACTIVA.
    def getSecciones(self):
        data = []
        guia = self.getGuia()
        secciones = seccion.objects.filter(guia_id=guia.id)
        for i in secciones:
            data.append(i.id)
        return data

    # FUNCION PARA OBTENER LA SECCION COMO CLAVE Y LOS GRUPOS DE PREGUNTAS CORRESPONDIENTE A ESA SECCION COMO VALOR.
    def getDatos(self):
        guia = self.getGuia()
        data = {}
        secciones = seccion.objects.filter(guia_id=guia.id)
        for i in secciones:
            data[i.nombre] = self.getGrupoIndicador(i.id)
            data.copy()
        return data

    # FUNCION PARA OBTENER A PARTIR DE UNA SECCION TODOS SUS GRUPOS DE PREGUNTAS.
    def getGrupoIndicador(self, idSeccion):
        aux = []
        # PARA CUANDO LA SECCION SI TIENE GRUPOS DE PREGUNTAS ASOCIADOS ( IDENTIFICACION Y SOBRE ENTIDAD)
        if clasificadorIndicadores.objects.filter(seccion_id=idSeccion).exists():
            grupoInd = clasificadorIndicadores.objects.filter(seccion_id=idSeccion)
            for i in grupoInd:
                aux.append(i)
                self.getIndicador(i, aux)
            return aux
        # PARA CUANDO LA SECCION NO TIENE GRUPOS DE PREGUNTAS ASOCIADOS (LAS DEMAS SECCIONES)
        else:
            secciones = self.getSecciones()
            for i in secciones:
                if i == idSeccion:
                    query = seccion.objects.get(id=i)
                    aux.append(query)
            return aux

    # FUNCION PARA A PARTIR DE UN GRUPO DE PREGUNTAS OBTENER TODAS SUS PREGUNTAS
    def getIndicador(self, i, aux):
        indicadores = Indicadores.objects.filter(clasificadorIndicadores_id=i.id)[::-1]
        for i in indicadores:
            aux.append(i)

    '''FUNCION PARA OBTENER LAS COLUMNAS DE UNA SECCION(NO DEBE APLICAR PARA IDENTIFICACION Y SOBRE ENTIDAD),
    SE OBTIENE LA SECCION COMO CLAVE Y LAS COLUMNAS COMO VALOR'''
    def getCol(self):
        data ={}
        secciones = self.getSecciones()
        for i in secciones:
            col = nomencladorColumna.objects.filter(seccion_id=i)
            data[i] = col
            data.copy()
        return data

    '''FUNCION PARA OBTENER LAS INTANCIAS DE UNA SECCION(NO DEBE APLICAR PARA IDENTIFICACION Y SOBRE ENTIDAD),
        SE OBTIENE LA SECCION COMO CLAVE Y LAS INTANCIAS COMO VALOR.'''
    def getInstancias(self):
        data = {}
        secciones = self.getSecciones()
        for i in secciones:
            obj = instanciaSeccion.objects.filter(seccion_id=i)
            data[i] = obj
            data.copy()
        return data


# PROCEDIMIENTO PARA CREAR EL UNIVERSO.
class crearUniversoView(LoginRequiredMixin, CreateView):
    template_name = 'entidad/crearUniverso.html'
    model = universoEntidades
    form_class = universoForm
    success_url = reverse_lazy('guia:listarUniverso')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Creacion de universo'
        context['tituloPestaña'] = 'SCIE | Universo'
        return context

# PROCEDIMIENTO PARA ACTUALIZAR EL UNIVERSO.
class updateUniversoView(LoginRequiredMixin, UpdateView):
    model = universoEntidades
    form_class = universoForm
    template_name = 'entidad/crearUniverso.html'
    success_url = reverse_lazy('guia:listarUniverso')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Edicion de universo'
        context['tituloPestaña'] = 'SCIE | Universo'
        return context

# PROCEDIMIENTO PARA LISTAR EL UNIVERSO.
class listarUniversoView(LoginRequiredMixin, ListView):
    model = universoEntidades
    template_name = 'entidad/listarUniverso.html'
    context_object_name = 'universo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Universos definidos'
        context['tituloPestaña'] = 'SCIE | Universo'
        return context

# PROCEDIMIENTO PARA ELIMINAR EL UNIVERSO.
class eliminarUniverso(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        universo = get_object_or_404(universoEntidades, id=self.kwargs['pk'])
        universo.delete()
        messages.success(self.request, "La entidad " + universo.entidad_codigo.nombre_CI + " ha sido eliminada del universo correctamente.")
        return redirect('guia:listarUniverso')

# PROCEDIMIENTO PARA CREAR EL UNIVERSO A PARTIR DE LAS ENTIDADES QUE HAYAN SIDO SELECCIONADAS EN LA TABLA DE ENTIDADES.
class dataUniversoView(LoginRequiredMixin, TemplateView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        listaEnitdadesSelected = json.loads(request.POST['data'])
        try:
            aux = []
            for i in listaEnitdadesSelected:
                query = Entidad.objects.get(id=i['id'])
                aux.append(query)
            data['exito'] = self.crearUniverso(aux)
        except Exception as e:
            data['error'] =str(e)
        return JsonResponse(data, safe=False)

    def crearUniverso(self, listaEntidades):
        guia = guiaEstadistica.objects.get(activo=True)
        sms = 'Universo creado correctamente.'
        if universoEntidades.objects.count() == 0:
            for i in listaEntidades:
                    objUniverso = universoEntidades(
                        guia=guia,
                        entidad_codigo=i
                    )
                    objUniverso.save()
            return sms
        for i in listaEntidades:
            try:
                universoEntidades.objects.get(entidad_codigo=i)
            except:
                objUniverso = universoEntidades(
                    guia=guia,
                    entidad_codigo=i
                )
                objUniverso.save()
        return sms

# PROCEDIMIENTO PARA CREAR LAS PREGUNTAS EVALUADAS Y LAS INSTANCIAS DE SECCION
class dataCaptacion(captarDatosView):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        campos = dict(request.POST)
        action = campos.get('action')
        entidad = campos.get('Entidad')
        try:
            # PARTE PARA CREAR PREGUNTAS EVALUADAS
            if action[0] == 'dataCaptacion':
                objCuestionario = self.createCuestionario(entidad)
                if objCuestionario == False:
                    data['error'] = 'La entidad seleccionada ya ha sido controlada.'
                else:
                    for clave, valor in campos.items():
                        if clave != 'action' and clave != 'Entidad':
                            preguntaEvaluada = PreguntasEvaluadas(
                                captacion_id=objCuestionario,
                                pregunta=Indicadores.objects.get(id=int(clave)),
                                respuesta=valor[0]
                            )
                            preguntaEvaluada.save()
                    data['exito'] = 'Los datos han sido captados correctamente.'
            # PARTE PARA CREAR LAS INSTANCIAS
            if action[0] == 'crearInstancia':
                objSeccion = seccion.objects.get(id=request.POST['seccion_id'])
                lastCuestionario = cuestionario.objects.last()
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
                    data['sms'] = 'Se ha creado y guardado el registro de manera correcta.'
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
                    data['sms'] = 'Se ha creado y guardado el registro de manera correcta.'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def createCuestionario(self, entidad):
        try:
            query = Entidad.objects.get(nombre_CI__exact=entidad[0])
            objCuestionario = cuestionario(
                    guia=self.getGuia(),
                    entidad_codigo=query
                )
            objCuestionario.save()
            return objCuestionario
        except:
            return False

# PROCEDIMIENTO PARA MOSTRAR EL LISTADO DE LOS CUESTIONARIOS CAPTADOS SEGUN EL PERMISO DEL USUARIO
class guiaCaptada(LoginRequiredMixin, ListView):
    template_name = 'guiaEstadistica/guiaCaptada.html'
    model = cuestionario
    context_object_name = 'cuestionarios'

    def getPermisoEstadistico(self):
        if self.request.user.has_perm('usuario.estadistico'):
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cuestionarios'] = getCuestionarios(self.request.user)
        context['permisoEstadistico'] = self.getPermisoEstadistico()
        context['titulo'] = 'Cuestionarios captados'
        context['tituloPestaña'] = 'SCIE | Cuestionarios'
        return context

# PROCEDIMIENTO PARA ELIMINAR UN CUESTIONARIO CAPTADO
class eliminarGuiaCaptada(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        guia = get_object_or_404(cuestionario, id=self.kwargs['pk'])
        guia.delete()
        messages.success(self.request,"El cuestionario captado a " + guia.entidad_codigo.nombre_CI + " ha sido eliminado correctamente.")
        return redirect('guia:guiaCaptada')

# PROCEDIMIENTO PARA OBTENER LA INFORMACION DE UN CUESTIONARIO CAPTADO
class informacionCaptada(LoginRequiredMixin, TemplateView):

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

# PROCEDIMIENTO PARA OBTENER LAS INSTANCIAS DE LAS SECCIONES CAPTADAS
class seccionCaptada(LoginRequiredMixin, TemplateView):

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

# PROCEDIMIENTO PARA CREAR UNA GUIA CON LA MISMA CONFIGURACION DE OTRA YA EXISTENTE
class crearGuiaDefinida(LoginRequiredMixin, TemplateView):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        activo = None
        query = guiaEstadistica.objects.all()
        action = request.POST['action']
        if request.POST['activo'] == 'true':
            activo = True
            for i in query:
                i.activo = False
                i.save()
        else:
            activo = False
        try:
            if action == 'creacionDeGuia':
                guiaNueva=guiaEstadistica(
                    nombre=request.POST['guiaNueva'],
                    activo=activo
                )
                guiaNueva.save()
                query_secciones = seccion.objects.filter(guia_id__nombre=request.POST['guiaYaDefinida'])
                for i in query_secciones:
                    # PARA PODER CREAR LAS SECCIONES DE IDENTIFICACION Y SOBRE ENTIDAD
                    if i.tipo == 1 or i.tipo == 2:
                        aux = seccion(
                            nombre=i.nombre,
                            guia_id=guiaNueva,
                            periodo_id=None,
                            numero=None,
                            subNumero=None,
                            orden=i.orden,
                            activo=i.activo,
                            tipo=i.tipo
                        )
                        aux.save()
                        self.crearGrupoPreguntas(i, guiaNueva)
                    # PARA PODER CREAR EL RESTO DE LAS SECCIONES
                    else:
                       aux=seccion(
                            nombre=i.nombre,
                            guia_id=guiaEstadistica.objects.get(id=guiaNueva.id),
                            periodo_id=clasificadorPeriodo.objects.get(id=i.periodo_id.id),
                            numero=i.numero,
                            subNumero=i.subNumero,
                            orden=i.orden,
                            activo=i.activo,
                            tipo=i.tipo
                        )
                       aux.save()
                data['exito'] = 'La guia '+ guiaNueva.nombre + 'ha sido creada correctamente.'
            else:
                data['error'] = 'error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    # FUNCION PARA CREAR EN LA GUIA NUEVA LOS MISMO GRUPO DE PREGUNTAS QUE TIENE LA GUIA DEFINIDA
    def crearGrupoPreguntas(self, objSeccion, guia):
        query = seccion.objects.filter(guia_id__id=guia.id)
        for i in query:
            if i.nombre == objSeccion.nombre:
                grupoPreguntas = clasificadorIndicadores.objects.filter(seccion_id__id=objSeccion.id)
                for j in grupoPreguntas:
                    aux = clasificadorIndicadores(
                        seccion_id=seccion.objects.get(id=i.id),
                        nombre=j.nombre,
                        activo=True
                    )
                    aux.save()
                    self.crearPreguntas(j, aux)

    # FUNCION PARA CREAR EN LA GUIA NUEVA LAS MISMAS PREGUNTAS QUE TIENE LA GUIA DEFINIDA
    def crearPreguntas(self, grupoPreguntaGuiaDefinida, grupoPreguntaGuiaNueva):
        query = Indicadores.objects.filter(clasificadorIndicadores_id__id=grupoPreguntaGuiaDefinida.id)
        if grupoPreguntaGuiaDefinida.nombre == grupoPreguntaGuiaNueva.nombre:
            for i in query:
                if i.cod_indicador == None:
                    try:
                        aux = Indicadores(
                            clasificadorIndicadores_id=clasificadorIndicadores.objects.get(id=grupoPreguntaGuiaNueva.id),
                            nombre=i.nombre,
                        )
                        aux.save()
                        self.asignarRespuesta(aux, i.respuestas_id.all())
                    except:
                        print('error')
                else:
                    try:
                        aux = Indicadores(
                            clasificadorIndicadores_id=clasificadorIndicadores.objects.get(id=grupoPreguntaGuiaNueva.id),
                            nombre=i.nombre,
                            cod_indicador=i.cod_indicador
                        )
                        aux.save()
                        self.asignarRespuesta(aux, i.respuestas_id.all())
                    except:
                        print('error')

    # FUNCION PARA ASIGNAR LAS RESPUESTAS CORRESPONDIENTES A CADA PREGUNTAS.
    def asignarRespuesta(self, preguntaNueva, listaRespuestasDefinidas):
        for i in listaRespuestasDefinidas:
            preguntaNueva.respuestas_id.add(i)

# PROCEDIMIENTO PARA EL REPORTE GENERAL EN EXCEL.
class reporteGeneralExcel(LoginRequiredMixin, TemplateView):

    template_name = 'reportes/general.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Reporte General'
        context['tituloPestaña'] = 'SCIE | Reportes'
        context['grupoPreguntas'] = self.getGrupoPreguntas()
        context['cuestionarios'] = getCuestionarios(self.request.user)
        return context

    def getGrupoPreguntas(self):
        data = {}
        query = clasificadorIndicadores.objects.filter(seccion_id__guia_id__activo=True)
        for i in query[1:]:
            data[i.id] = i.nombre
        return data

# PROCEDIMIENTO PARA EL REPORTE EXCEL DE VERIFICACION DE LOS INDICADORES
class reporteVerificacionIndicadores(LoginRequiredMixin, TemplateView):
    template_name = 'reportes/verificacion.html'

     #Esta funcion es para trabajar con las infomacion de las verificaciones de manera general
    def getDiccionarioSecciones(self):
        data = {}
        secciones = seccion.objects.filter(guia_id__activo=True)
        for j in secciones:
            if j.numero != None:
                data[j.nombre] = j.numero
        return data

    # Esta otra funcion es para trabajar con las infomacion de las verificaciones de cada cuestionario captado
    def getSeccionesGuia(self):
        return seccion.objects.filter(guia_id__activo=True)[2:]


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Reporte Total'
        context['tituloPestaña'] = 'SCIE | Reportes'
        context['secciones'] = self.getDiccionarioSecciones()
        context['seccionesGuias'] = self.getSeccionesGuia()
        context['cuestionarios'] = getCuestionarios(self.request.user)
        return context

# PROCEDIMIENTO PARA EL REPORTE EXCEL DE DISCIPLINA INFORMATIVA
class reporteDisciplinaInformativa(LoginRequiredMixin, TemplateView):
    template_name = 'reportes/disciplinaInformativa.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Reporte de Disciplina Informativa'
        context['tituloPestaña'] = 'SCIE | Reportes'
        context['cuestionarios'] = getCuestionarios(self.request.user)
        return context

# PROCEDIMIENTO PARA EL REPORTE EXCEL DE SENALAMIENTOS DE ERRORES
class reporteSeñalamientosErrores(reporteDisciplinaInformativa):
    template_name = 'reportes/señalamientosErrores.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Reporte de Señalamientos Errores'
        context['tituloPestaña'] = 'SCIE | Reportes'
        return context

# PROCEDIMIENTO PARA EL REPORTE EXCEL DE DOMICILIO SOCIAL INCORRECTO
class reporteDomicilioSocial(reporteDisciplinaInformativa):
    template_name = 'reportes/domicilioSocial.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Reporte de Domicilio Social Incorrecto'
        context['tituloPestaña'] = 'SCIE | Reportes'
        return context

# PROCEDIMIENTO PARA EL REPORTE DEL UNIVERSO DE LA GUIA
class reporteUniversoGuia(reporteDisciplinaInformativa):
    template_name = 'reportes/universoGuia.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Reporte del Universo de la Guia'
        context['tituloPestaña'] = 'SCIE | Reportes'
        context['universo'] = getUniverso(self.request.user)
        return context

# PROCEDIMIENTO PARA EL REPORTE DE CAPTACION
class reporteCaptacion(reporteDisciplinaInformativa):
    template_name = 'reportes/captacion.html'

    def getCINoCaptados(self, listaDeCaptados):
        idsAExcluir = []
        listaNoCaptados = []
        universo = getUniverso(self.request.user)
        for i in listaDeCaptados:
            idsAExcluir.append(i.entidad_codigo)
        for j in universo.exclude(entidad_codigo__in=idsAExcluir):
            listaNoCaptados.append(j)
        return listaNoCaptados

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Reporte de Captacion'
        context['tituloPestaña'] = 'SCIE | Reportes'
        context['noCaptados'] = self.getCINoCaptados(context['cuestionarios'])

        return context

# PROCEDIMIENTO PARA MODIFICAR LAS PREGUNTAS CAPTADAS (IDENTIFICACION Y SOBRE ENTIDAD)
class modificarPreguntasView(captarDatosView):

    template_name = 'guiaEstadistica/captardatos.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        campos = dict(request.POST)
        print(campos)
        try:
            if action == 'editarDataCaptacion':
                query = PreguntasEvaluadas.objects.filter(captacion_id__id=campos['idCuestionario'][0])
                for clave, valor in campos.items():
                    if clave != 'action' and clave != 'idCuestionario':
                        self.editarRespuesta(query, clave, valor[0])
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def editarRespuesta(self, listaPreguntas, clave, valor):
        for i in listaPreguntas:
            if i.pregunta == clave:
                i.respuesta = valor
                #i.save()

    def getPreguntasEvaluadas(self):
        data = {}
        query = PreguntasEvaluadas.objects.filter(captacion_id__id=self.kwargs['pk'])
        for i in query:
            data[i] = i.respuesta
            data.copy()
        return data

    def getCuestionario(self):
        return cuestionario.objects.get(id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'editPreguntas'
        context['titulo'] = 'Modificar las siguientes secciones del cuestionario captado a:'
        context['tituloPestaña'] = 'SCIE | Edicion-Preguntas'
        context['cuestionario'] = self.getCuestionario()
        context['preguntas'] = self.getPreguntasEvaluadas()
        return context

# PROCEDIMIENTO PARA CONTINUAR CON LA CAPTACION DEL RESTO DE LAS SECCIONES
class continuarCaptacionView(captarDatosView):

    template_name = 'guiaEstadistica/captardatos.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'continuarCaptacion':
                objSeccion = seccion.objects.get(id=request.POST['seccion_id'])
                quey_cuestionario = cuestionario.objects.get(id=request.POST['cuestionario'])
                if objSeccion.periodo_id.tipo == "Anual":
                    instancia = instanciaSeccion(
                        seccion_id_id=request.POST['seccion_id'],
                        cuestionario_fk=quey_cuestionario,
                        codigo_id_id=request.POST['codigo_id'],
                        columna_id_id=request.POST['columna_id'],
                        registro_1=request.POST['registro_1'],
                        registro_2=None,
                        registro_3=None,
                        modelo_1=request.POST['modelo_1'],
                        modelo_2=None,
                        modelo_3=None,
                    )
                    data['sms'] = 'Se ha creado y guardado el registro de manera correcta.'
                    instancia.save()
                else:
                    instancia = instanciaSeccion(
                        seccion_id_id=request.POST['seccion_id'],
                        cuestionario_fk=quey_cuestionario,
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
                    data['sms'] = 'Se ha creado y guardado el registro de manera correcta.'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def getCuestionario(self):
        return cuestionario.objects.get(id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'continuarCaptacion'
        context['titulo'] = 'Continuar la captacion de infomacion a:'
        context['tituloPestaña'] = 'SCIE | Captacion'
        context['cuestionario'] = self.getCuestionario()
        return context

