#import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import connection
from django.contrib import messages
from django.utils.encoding import smart_str
from django.contrib.auth.decorators import login_required
from reconocimiento_deportivo.forms.solicitudes import ReconocimientoDeportivoForm, AdjuntoReconocimientoForm, DiscusionForm
from reconocimiento_deportivo.modelos.respuestas import ListaSolicitudesReconocimiento
from reconocimiento_deportivo.modelos.solicitudes import ReconocimientoDeportivo, AdjuntoReconocimiento, DiscusionReconocimiento
from solicitudes_escenarios.utilities import comprimir_archivos
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
        form = ReconocimientoDeportivoForm(request.POST, instance=reconocimiento)

        if form.is_valid():
            nueva_solicitud = form.save()

            if not reconocimiento:
                connection.set_tenant(nueva_solicitud.para_quien)
                ListaSolicitudesReconocimiento.objects.create(solicitud=nueva_solicitud.id, entidad_solicitante=entidad).save()
                connection.set_tenant(entidad)

            request.session['identidad'] = {
                'id_solicitud': nueva_solicitud.id,
                'id_entidad': entidad.id,
                'estado': True
            }
            return redirect('adjuntar_requerimientos_reconocimiento', nueva_solicitud.id)

    return render(request,'wizard/wizard_reconocimiento.html',{
        'form': form,
        'wizard_stage': 1
    })


@login_required
#@permission_required('solicitud.add_solicitudescenario')
def cancelar_solicitud(request, reconocimiento_id=None):
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
def ver_solicitud(request, reconocimiento_id):
    """
    Abril 9, 2016
    Autor: Karent Narvaez

    Permite tener el detalle de una solicitud

    """
    try:
        solicitud = ReconocimientoDeportivo.objects.get(id = reconocimiento_id)
    except:
        messages.error(request,'No existe la solicitud')
        return redirect('listar_reconocimientos')

    solicitud.codigo_unico = solicitud.codigo_unico(request.tenant)
    discusiones = DiscusionReconocimiento.objects.filter(solicitud = solicitud)

    return render(request,'ver_solicitud_reconocimiento.html',{
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
    discusiones = DiscusionReconocimiento.objects.filter(solicitud=solicitud)

    return render(request,'imprimir_reconocimiento.html',{
        'solicitud' : solicitud,
        'discusiones' : discusiones
    })


@login_required
#@permission_required('solicitud.add_solicitudescenario')
def adjuntar_requerimientos(request, reconocimiento_id):
    """
    Abril 12,2016
    Autor: Karent Narvaez

    Permite adjuntar archivos  de los requerimientos a las solicitudes de reconocimiento deportivo que estan en actual creacion. se verifica la autenticidad de la peticion
    :param reconocimiento_id: id de la solicitud a la que se van a adjuntar archivos
    """

    try:
        solicitud = ReconocimientoDeportivo.objects.get(id=reconocimiento_id)
    except:
        messages.error(request,'Solicitud no encontrada')
        return redirect('listar_solicitudes')
        
    adjuntos = solicitud.adjuntos()

    #Se verifica la autenticidad de la solicitud
    try:
        auth = request.session['identidad']
        if not auth['estado'] or auth['id_solicitud'] != int(reconocimiento_id) or auth['id_entidad'] != request.tenant.id:
            raise Exception
    except Exception:
        messages.error(request,'Estas intentando editar una solicitud que ya fue enviada')
        return redirect('listar_reconocimientos')

    form = AdjuntoReconocimientoForm()

    if request.method == 'POST':
        form = AdjuntoReconocimientoForm(request.POST, request.FILES)
        if form.is_valid():
            adjuntos = form.save(commit=False)
            adjuntos.solicitud = solicitud
            adjuntos.archivo = solicitud
            adjuntos.save()
            return redirect('adjuntar_requerimientos_reconocimiento', solicitud.id)

    return render(request,'wizard/wizard_adjuntos.html',{
        'form' : form,
        'reconocimiento_id': reconocimiento_id,
        'wizard_stage': 2,
        'adjuntos': adjuntos
    })


@login_required
#@permission_required('solicitud.add_solicitudescenario')
def borrar_adjunto(request, reconocimiento_id, adjunto_id):
    """
    Abril 13, 2016
    Autor: Karent Narvaez

    Permite borrar archivos adjuntos asociados a una solicitud de reconocimiento deportivo. Se valida la autenticidad de la petición

    :param reconocimiento_id: id de la solicitud a borrar adjunto
    :param adjunto_id: id del adjunto a borrar
    """
    try:
        adjunto = AdjuntoReconocimiento.objects.get(id=adjunto_id, solicitud=reconocimiento_id)
    except Exception:
        messages.error(request,'No existe el archivo adjunto, no se ha realizado ninguna accion')
        return redirect('adjuntar_requerimientos_reconocimiento', reconocimiento_id)

    #Se verifica la autenticidad de la solicitud
    try:
        auth = request.session['identidad']
        if not auth['estado'] or auth['reconocimiento_id'] != int(reconocimiento_id) or auth['id_entidad'] != request.tenant.id:
            raise Exception
    except Exception:
        messages.error(request,'Estas intentando editar una solicitud que ya fue enviada')
        return redirect('listar_reconocimientos')

    adjunto.delete()
    messages.success(request,'Archivo adjunto eliminado satisfactoriamente')
    return redirect('adjuntar_requerimientos_reconocimiento', reconocimiento_id)


@login_required
#@permission_required('solicitud.add_solicitudescenario')
def finalizar_solicitud(request, solicitud_id):
    """
    Abril 13, 2016
    Autor: Karent Narvaez

    Permite guardar y completar la creacion de solicitud. 
    :param solicitud_id: id de la solicitud en creacion
    """
    try:
        solicitud = ReconocimientoDeportivo.objects.get(id=id)
        solicitud.estado = 0
        solicitud.save()
        messages.success(request,'Solicitud enviada con éxito a:'+str(solicitud.para_quien))
        del request.session['identidad']
    except:
        messages.error(request,'Solicitud no encontrada')

    return redirect('listar_reconocimientos')


@login_required
#@permission_required('solicitud.add_solicitudescenario')
def editar_solicitud(request, reconocimiento_id):
    """
    Abril 13, 2016
    Autor: Karent Narvaez

    Permite cargar la plantilla de edicion de solicitudes

    """
    try:
        solicitud = ReconocimientoDeportivo.objects.get(id=reconocimiento_id)
    except:
        messages.error(request,'No existe la solicitud')
        return redirect('listar_solicitudes')

    solicitud.codigo_unico = solicitud.codigo_unico(request.tenant)
    discusiones = DiscusionReconocimiento.objects.filter(solicitud=solicitud)
    form = DiscusionForm()
    form_adjunto = AdjuntoReconocimientoForm()

    return render(request,'ver_solicitud_reconocimiento.html',{
        'solicitud' : solicitud,
        'discusiones' : discusiones,
        'form_comentarios' : form,
        'form_adjunto' : form_adjunto,
        'responder' : True
    })


@login_required
#@permission_required('solicitud.add_solicitudescenario')
def enviar_comentario(request, id):
    """
    Abril 13, 2016
    Autor: Karent Narvaez

    Permite volver a enviar la solicitud completa
    """
    if request.method == 'POST':

        try:
            solicitud = ReconocimientoDeportivo.objects.get(id=id)
        except:
            messages.error(request,'No existe la solcitud')
            return redirect('listar_solicitudes')

        form = DiscusionForm(request.POST)
        form_adjunto = AdjuntoReconocimientoForm(request.POST, request.FILES)

        if form.is_valid():
            discusion = form.save(commit=False)
            discusion.solicitud = solicitud
            discusion.estado_anterior = solicitud.estado
            discusion.estado_actual = 0
            discusion.entidad = request.tenant
            discusion.respuesta = False
            discusion.save()

            if form_adjunto.is_valid():
                adjunto = form_adjunto.save(commit=False)
                adjunto.solicitud = solicitud
                adjunto.discusion = discusion
                adjunto.save()

            solicitud.estado = discusion.estado_actual
            solicitud.save()
            messages.success(request,'La solicitud se ha reenviado con exito')
            return redirect('ver_solicitud_reconocimiento', solicitud.id)

        messages.error(request,'La solicitud no se ha podido reenviar por un error en el formulario, intentalo de nuevo')
        return redirect('editar_solicitud_reconocimiento', solicitud.id)


@login_required
def descargar_adjuntos(request, reconocimiento_id):
    """
    Abril 13, 2016
    Autor: Karent Narvaez

    Permite descargar todos los adjuntos de una solicitud en un archivo zip

    """

    adjuntos = AdjuntoReconocimiento.objects.filter(solicitud = reconocimiento_id)
    directorio = '/adjuntos_reconocimiento_deportivo/'
    zip,temp = comprimir_archivos(adjuntos, directorio)
    response = HttpResponse(zip,content_type="application/zip")
    response['Content-Disposition'] = 'attachment; filename=adjuntos_solicitud_%s.zip'%(adjuntos[0].solicitud.codigo_unico(request.tenant))
    temp.seek(0)
    response.write(temp.read())
    return response


@login_required
def descargar_adjunto(request, reconocimiento_id, adjunto_id):
    """
    Abril 13, 2016
    Autor: Daniel Correa

    Permite descargar algun archivo adjunto de una solicitud reconocimiento deportivo

    """
    try:
        adjunto = AdjuntoReconocimiento.objects.get(solicitud = reconocimiento_id, id = adjunto_id)
    except:
        messages.error(request,'No existe el archivo adjunto solicitado')
        return redirect('listar_reconocimientos')

    response = HttpResponse(adjunto.archivo.read(),content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(adjunto.nombre_archivo())
    response['X-Sendfile'] = smart_str(adjunto.archivo)
    return response


@login_required
def descargar_adjunto_discusion(request, reconocimiento_id, discusion_id):
    """
    Abril 14, 2016
    Autor: Karent Narvaez

    Permite descargar los archivos adjuntos de una discusion a una solicitud
    """
    directorio = '/adjuntos_reconocimiento_deportivo/'    
    adjunto = AdjuntoReconocimiento.objects.get(solicitud = reconocimiento_id, discucion = discusion_id)
    zip,temp = comprimir_archivos(adjunto, directorio)
    response = HttpResponse(zip,content_type="application/zip")
    response['Content-Disposition'] = 'attachment; filename=adjuntos_solicitud_%s.zip'%(adjunto[0].solicitud.codigo_unico(request.tenant))
    temp.seek(0)
    response.write(temp.read())
    return response