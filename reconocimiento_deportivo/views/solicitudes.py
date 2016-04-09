#import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import connection
from django.contrib import messages
#from django.utils.encoding import smart_str
from django.contrib.auth.decorators import login_required
#from reconocimiento_deportivo.utilities import comprimir_archivos
from reconocimiento_deportivo.forms.solicitudes import ReconocimientoDeportivoForm#, AdjuntoSolicitudForm, EditarForm
#from reconocimiento_deportivo.modelos.respuestas import ListaSolicitudesReconocimiento
from reconocimiento_deportivo.modelos.solicitudes import ReconocimientoDeportivo#, AdjuntoSolicitud, DiscucionReconocimiento
# Create your views here.

@login_required
#@permission_required('solicitud.add_solicitudescenario')
def solicitar(request,reconocimiento_id=None):
    """
    Abril 9, 2016
    Autor: Karent Narvaez

    Permite crear una solicitud con sus datos basicos
    """

    try:
        reconocimiento = ReconocimientoDeportivo.objects.get(id=reconocimiento_id)
    except Exception:
        reconocimiento = None

    form = ReconocimientoDeportivoForm(instance=reconocimiento)

    if request.method == 'POST':
        entidad = request.tenant
        form = ReconocimientoDeportivoForm(request.POST,instance=reconocimiento)

        if form.is_valid():
            nueva_solicitud = form.save()

            if not reconocimiento:
                connection.set_tenant(nueva_solicitud.para_quien)
                ListaSolicitudes.objects.create(solicitud=nueva_solicitud.id,entidad_solicitante=entidad).save()
                connection.set_tenant(entidad)

            request.session['identidad'] = {
                'id_solicitud': nueva_solicitud.id,
                'id_entidad': entidad.id,
                'estado': True
            }
            return redirect('adjuntar_archivo_solicitud',nueva_solicitud.id)

    return render(request,'wizard/wizard_reconocimiento.html',{
        'form': form,
        'wizard_stage': 1
    })


@login_required
#@permission_required('solicitud.add_solicitudescenario')
def cancelar_solicitud_reconocimiento(request, reconocimiento_id=None):
    """
    Abril 9, 2016
    Autor: Karent Narvaez

    Permite cancelar una solicitud al momento de estarse creando o luego de estar creada
    :param request:
    :param reconocimiento_id:
    :return:
    """
    if reconocimiento_id:
        try:
            solicitud = ReconocimientoDeportivo.objects.get(id=reconocimiento_id)
            solicitud.estado = 4
            solicitud.save()
        except Exception:
            messages.error(request,'No existe la solicitud, proceso no realizado')  
            
    try:
        del request.session['identidad']
    except Exception:
        pass

    messages.warning(request,'Solicitud cancelada correctamente')
    return redirect('listar_reconocimientos')


@login_required
def listar_reconocimientos(request):
    """
    Abril 9, 2016
    Autor: Karent Narvaez

    Permite listar las solicitudes de reconocimiento deportivo que ha hecho un club dado

    """
    solicitudes = ReconocimientoDeportivo.objects.all()
    for solicitud in solicitudes:
        solicitud.codigo = solicitud.codigo_unico(request.tenant)
    return render(request,'lista_reconocimientos.html',{
        'solicitudes': solicitudes
    })


@login_required
def ver_solicitud(request,id):
    """
    Abril 9, 2016
    Autor: Karent Narvaez

    Permite tener el detalle de una solicitud

    """
    try:
        solicitud = ReconocimientoDeportivo.objects.get(id=id)
    except:
        messages.error(request,'No existe la solicitud')
        return redirect('listar_reconocimientos')

    solicitud.codigo_unico = solicitud.codigo_unico(request.tenant)
    discusiones = DiscucionReconocimiento.objects.filter(solicitud=solicitud)
    #for escenario in solicitud.escenarios.all(): escenario.fotos = Foto.objects.filter(escenario=escenario)

    return render(request,'ver_solicitud.html',{
        'solicitud' : solicitud,
        'discusiones' : discusiones
    })


@login_required
def imprimir_solicitud(request,reconocimiento_id):
    """
    Abril 9, 2016
    Autor: Karent Narvaez

    Permite renderizar el html imprimible de la solicitud

    """
    try:
        solicitud = ReconocimientoDeportivo.objects.get(id=reconocimiento_id)
    except:
        messages.error(request,'No existe la solicitud')
        return redirect('listar_reconocimientos')

    solicitud.codigo_unico = solicitud.codigo_unico(request.tenant)
    discusiones = DiscucionReconocimiento.objects.filter(solicitud=solicitud)

    return render(request,'solicitud_imprimir.html',{
        'solicitud' : solicitud,
        'discusiones' : discusiones
    })

