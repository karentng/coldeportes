from datetime import datetime, timedelta
from django.db import connection
from django.contrib import messages
from django.utils.encoding import smart_str
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from entidades.models import Club
from reconocimiento_deportivo.modelos.respuestas import ListaSolicitudesReconocimiento
from reconocimiento_deportivo.modelos.solicitudes import ReconocimientoDeportivo, DiscusionReconocimiento, AdjuntoReconocimiento
from reconocimiento_deportivo.forms.respuesta import ResponderSolicitudForm
from solicitudes_escenarios.utilities import comprimir_archivos


@login_required
@permission_required('reconocimiento_deportivo.view_listasolicitudesreconocimiento')
def listar_solicitudes_reconocimientos(request):
    """
    Abril 19, 2016
    Autor: Karent Narvaez

    Permite listar las solicitudes completas para el ente

    """
    tenant_actual = request.tenant
    resultados = ListaSolicitudesReconocimiento.objects.all().order_by('fecha_creacion')
    resultados_finales = []
    dashboard = dict()
    dashboard['total_solicitudes'] = resultados.count()
    dashboard['total_rechazadas'] = 0
    dashboard['total_aprobadas'] = 0
    dashboard['total_esperando_respuesta'] = 0

    for resultado in resultados:
        entidad = resultado.entidad_solicitante
        solicitud_id = resultado.solicitud
        connection.set_tenant(entidad)
        solicitud_hecha = ReconocimientoDeportivo.objects.get(id = solicitud_id)
        #Solicitudes esperando respuesta
        if solicitud_hecha.estado == 0:
            solicitud_hecha.entidad_solicitante = entidad
            solicitud_hecha.codigo = solicitud_hecha.codigo_unico(entidad)
            tiempo_a_contestar = resultado.fecha_creacion + timedelta(days = 46)
            tiempo_restante = tiempo_a_contestar - datetime.now()
            solicitud_hecha.tiempo_restante = str(tiempo_restante.days)
            resultados_finales.append(solicitud_hecha)
        #Solicitudes aprobadas
        elif solicitud_hecha.estado == 2:
            dashboard['total_aprobadas'] += 1
        #Solicitudes aprobadas
        elif solicitud_hecha.estado == 3:
            dashboard['total_rechazadas'] += 1

    dashboard['total_esperando_respuesta'] = len(resultados_finales)


    connection.set_tenant(tenant_actual)
    return render(request,'respuesta/lista_solicitudes.html',{
        'solicitudes': resultados_finales,
        'dashboard': dashboard

    })



def obtener_datos_solicitud(request, solicitud_id, entidad_id):
    try:
        lista = ListaSolicitudesReconocimiento.objects.get(entidad_solicitante = entidad_id, solicitud = int(solicitud_id))
    except Exception:
        messages.error(request,'No existe la solicitud')
        return False, redirect('listar_solicitudes_reconocimientos_respuesta')

    tenant_actual = request.tenant
    entidad = lista.entidad_solicitante
    connection.set_tenant(entidad)

    solicitud = ReconocimientoDeportivo.objects.get(id = solicitud_id)
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
    discusiones = DiscusionReconocimiento.objects.filter(solicitud = solicitud_id)

    for discusion in discusiones:
        discusion.estado_actual = discusion.get_estado_actual_display()
        discusion.entidad_nombre = discusion.entidad.nombre
        #discusion.tiene_adjunto = discusion.tiene_adjunto()
    discusiones = [discusion.__dict__ for discusion in discusiones]
    connection.set_tenant(tenant_actual)

    return solicitud, discusiones


@login_required
def ver_solicitud_reconocimiento(request, solicitud_id, entidad_id):
    """
    Abril 21, 2016
    Autor: Karent Narvaez

    Permite tener el detalle de una solicitud recibida

    """
    solicitud, discusiones = obtener_datos_solicitud(request, solicitud_id, entidad_id)

    if not solicitud:
        return discusiones

    return render(request,'respuesta/ver_solicitud_reconocimiento_respuesta.html',{
        'solicitud' : solicitud,
        'discusiones' : discusiones,
        'responder' : False

    })


@login_required
def imprimir_solicitud(request, solicitud_id, entidad_id):
    """
    Abril 21, 2016
    Autor: Karent Narvaez

    Permite renderizar el html imprimible de la solicitud

    """
    solicitud, discusiones = obtener_datos_solicitud(request, solicitud_id, entidad_id)

    if not solicitud:
        return discusiones

    return render(request,'respuesta/imprimir_solicitud_reconocimiento_respuesta.html',{
        'solicitud' : solicitud,
        'discusiones' : discusiones
    })


@login_required
def descargar_adjunto(request, solicitud_id, adjunto_id, entidad_id):
    """
    Abril 21, 2016
    Autor: Karent Narvaez

    Permite descargar algun archivo adjunto de una solicitud recibida

    """
    try:
        solicitud_reconocimiento = ListaSolicitudesReconocimiento.objects.get(entidad_solicitante = entidad_id, solicitud = int(solicitud_id))
    except:
        messages.error(request,'No existe la solicitud')
        return redirect('listar_solicitudes_reconocimientos')

    tenant_actual = request.tenant
    entidad = solicitud_reconocimiento.entidad_solicitante
    connection.set_tenant(entidad)

    try:
        adjunto = AdjuntoReconocimiento.objects.get(solicitud = solicitud_id, id = adjunto_id)
    except:
        messages.error(request,'No existe el archivo adjunto solicitado')
        return redirect('listar_solicitudes_reconocimientos')

    response = HttpResponse(adjunto.archivo.read(),content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(adjunto.nombre_archivo())
    response['X-Sendfile'] = smart_str(adjunto.archivo)

    connection.set_tenant(tenant_actual)
    return response


@login_required
@permission_required('reconocimiento_deportivo.add_listasolicitudesreconocimiento')
def responder_solicitud_reconocimiento(request, solicitud_id, entidad_id):
    """
    Abril 19, 2016
    Autor: Karent Narvaez

    Permite cargar la plantilla de respuestas de solicitudes

    """
    solicitud, discusiones = obtener_datos_solicitud(request, solicitud_id, entidad_id)

    if not solicitud:
        return discusiones

    form = ResponderSolicitudForm()

    return render(request,'respuesta/ver_solicitud_reconocimiento_respuesta.html',{
        'solicitud' : solicitud,
        'discusiones': discusiones,
        'form_comentarios' : form,
        'responder' : True
    })


def dar_reconocimiento_deportivo(club):
    """
    Abril 26, 2016
    Autor: Karent Narvaez

    Le da el reconocimiento deportivo a un club por 3 años
    """
    club = Club.objects.get(entidad_ptr = club)
    fecha_actual = datetime.now()
    club.fecha_vigencia =  datetime(fecha_actual.year + 5, 12, 31)
    club.reconocimiento = True
    club.save()


@login_required
@permission_required('reconocimiento_deportivo.add_listasolicitudesreconocimiento')
def enviar_respuesta(request, solicitud_id, entidad_id):
    """
    Abril 21, 2016
    Autor: Karent Narvaez

    Permite enviar la respuesta de una solicitud
    """
    if request.method == 'POST':

        try:
            solicitud_hecha = ListaSolicitudesReconocimiento.objects.get(entidad_solicitante = entidad_id, solicitud=int(solicitud_id))
        except:
            messages.error(request,'No existe la solicitud')
            return redirect('listar_solicitudes_reconocimientos')

        tenant_actual = request.tenant
        entidad = solicitud_hecha.entidad_solicitante
        connection.set_tenant(entidad)
        solicitud = ReconocimientoDeportivo.objects.get(id = solicitud_id)
        form = ResponderSolicitudForm(request.POST)

        if form.is_valid():
            discusion = form.save(commit=False)
            discusion.solicitud = solicitud
            discusion.estado_anterior = solicitud.estado
            discusion.entidad = tenant_actual
            discusion.respuesta = True
            discusion.save()

            for archivo in request.FILES.getlist('adjuntos'):
                 AdjuntoReconocimiento(solicitud = solicitud, archivo = archivo, discusion = discusion).save()

            solicitud.estado = discusion.estado_actual
            solicitud.save()
            #Si es aprobada la solicitud se da el reconocimiento deportivo al club
            if solicitud.estado == 2:
                dar_reconocimiento_deportivo(entidad)

            connection.set_tenant(tenant_actual)# se regresa al tenant del ente que respondió
            #solicitud_hecha.delete()# Se remueve del listado del ente            
            messages.success(request,'Su respuesta ha sido enviada con exito')
            return redirect('ver_solicitud_reconocimiento_respuesta', solicitud.id, entidad.id)

        connection.set_tenant(tenant_actual)
        messages.error(request,'Tu respuesta no se ha podido enviar por un error en el formulario, intenta de nuevo')
        return redirect('responder_solicitud', solicitud.id, entidad.id)


@login_required
def descargar_todos_adjuntos(request, solicitud_id, entidad_id):
    """
    Abril 21, 2016
    Autor: Karent Narvaez

    Permite descargar todos los adjuntos de una solicitud en un archivo zip

    """
    try:
        solicitud = ListaSolicitudesReconocimiento.objects.get(entidad_solicitante = entidad_id, solicitud = int(solicitud_id))
    except:
        messages.error(request,'No existe la solicitud')
        return redirect('listar_solicitudes_respuesta')

    tenant_actual = request.tenant
    entidad = solicitud.entidad_solicitante
    connection.set_tenant(entidad)

    directorio = '/adjuntos_reconocimiento_deportivo/'
    adjunto = AdjuntoReconocimiento.objects.filter(solicitud = solicitud_id)
    zip,temp = comprimir_archivos(adjunto, directorio)

    response = HttpResponse(zip,content_type="application/zip")
    response['Content-Disposition'] = 'attachment; filename=adjuntos_solicitud_%s.zip'%(adjunto[0].solicitud.codigo_unico(entidad))
    temp.seek(0)
    response.write(temp.read())
    connection.set_tenant(tenant_actual)

    return response


@login_required
def descargar_adjuntos_respuesta(request, solicitud_id, entidad_id, discusion_id):
    """
    Abril 21, 2016
    Autor: Karent Narvaez

    Permite descargar los archivos adjuntos de una respuesta a una solicitud
    """
    try:
        solicitud = ListaSolicitudesReconocimiento.objects.get(entidad_solicitante = entidad_id, solicitud = int(solicitud_id))
    except:
        messages.error(request,'No existe la solicitud')
        return redirect('listar_solicitudes_respuesta')

    tenant_actual = request.tenant
    entidad = solicitud.entidad_solicitante
    connection.set_tenant(entidad)

    directorio = '/adjuntos_reconocimiento_deportivo/'
    adjunto = AdjuntoRequerimientoReconocimiento.objects.filter(solicitud = solicitud_id, discusion = discusion_id)
    zip, temp = comprimir_archivos(adjunto, directorio)

    response = HttpResponse(zip,content_type="application/zip")
    response['Content-Disposition'] = 'attachment; filename=adjuntos_solicitud_%s.zip'%(adjunto[0].solicitud.codigo_unico(entidad))
    temp.seek(0)
    response.write(temp.read())
    connection.set_tenant(tenant_actual)

    return response