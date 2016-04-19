from datetime import datetime
from django.db import connection
from django.contrib import messages
from django.utils.encoding import smart_str
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required,permission_required
from reconocimiento_deportivo.modelos.respuestas import ListaSolicitudesReconocimiento
from reconocimiento_deportivo.modelos.solicitudes import ReconocimientoDeportivo


@login_required
def listar_solicitudes_reconocimientos(request):
    """
    Abril 19, 2016
    Autor: Karent Narvaez

    Permite listar las solicitudes completas para el ente

    """
    tenant_actual = request.tenant
    resultados = ListaSolicitudesReconocimiento.objects.all()
    resultados_finales = []
    tiempos_respuestas = dict()

    for resultado in resultados:
        entidad = resultado.entidad_solicitante
        solicitud_id = resultado.solicitud
        connection.set_tenant(entidad)
        solicitud_hecha = ReconocimientoDeportivo.objects.get(id = solicitud_id)
        solicitud_hecha.entidad_solicitante = entidad
        solicitud_hecha.codigo = solicitud_hecha.codigo_unico(entidad)
        diferencia = datetime.now()- solicitud_hecha.fecha_creacion
        tiempos_respuestas[solicitud_hecha.codigo] = str(diferencia.days)
        resultados_finales.append(solicitud_hecha)

    connection.set_tenant(tenant_actual)
    return render(request,'respuesta/lista_solicitudes.html',{
        'solicitudes': resultados_finales,
        'fechas': tiempos_respuestas,

    })


@login_required
#@permission_required('respuesta.add_listasolicitudes')
def responder_solicitud_reconocimiento(request, solicitud_id, entidad_id):
    """
    Abril 19, 2016
    Autor: Karent Narvaez

    Permite cargar la plantilla de respuestas de solicitudes

    """
    solicitud, discusiones = obtener_datos_solicitud(request, solicitud_id, entidad_id)

    if not solicitud:
        return discusiones

    form = DiscusionForm()
    return render(request,'ver_solicitud_reconocimiento_respuesta.html',{
        'solicitud' : solicitud,
        'discusiones': discusiones,
        'form_comentarios' : form,
        'responder' : True
    })


def obtener_datos_solicitud(request, solicitud_id, entidad_id):
    try:
        lista = ListaSolicitudesReconocimiento.objects.get(entidad_solicitante = entidad_id, solicitud = int(solicitud_id))
    except Exception:
        messages.error(request,'No existe la solicitud')
        return False,redirect('listar_solicitudes_reconocimientos_respuesta')

    yo = request.tenant
    entidad = lista.entidad_solicitante
    connection.set_tenant(entidad)

    solicitud = ReconocimientoDeportivo.objects.get(id=id)
    solicitud.entidad_solicitante = entidad
    solicitud.codigo_unico = solicitud.codigo_unico(entidad)
    adjuntos = solicitud.adjuntos()
    array = []

    for adjunto in adjuntos:
        resultado={
            'nombre_archivo' : adjunto.nombre_archivo(),
            'icon_extension' : adjunto.icon_extension(),
            'id' : adjunto.id
        }
        array.append(resultado)

    solicitud.adjuntos = array
    discusiones = DiscucionReconocimiento.objects.filter(solicitud=solicitud_id)

    for d in discusiones:
        d.estado_actual = d.get_estado_actual_display()
        d.entidad_nombre = d.entidad.nombre
        d.tiene_adjuntos = d.tiene_adjuntos()
    discusiones = [d.__dict__ for d in discusiones]
    connection.set_tenant(yo)

    return solicitud,discusiones