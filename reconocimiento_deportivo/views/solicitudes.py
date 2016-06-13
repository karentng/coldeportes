#import json
from datetime import datetime, timedelta, date
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import connection
from django.contrib import messages
from django.utils.encoding import smart_str
from django.contrib.auth.decorators import login_required, permission_required
from reconocimiento_deportivo.forms.solicitudes import ReconocimientoDeportivoForm, AdjuntoRequerimientoReconocimientoForm, DiscusionForm
from reconocimiento_deportivo.modelos.respuestas import ListaSolicitudesReconocimiento
from reconocimiento_deportivo.modelos.solicitudes import ReconocimientoDeportivo, AdjuntoRequerimientoReconocimiento, DiscusionReconocimiento
from solicitudes_escenarios.utilities import comprimir_archivos
# Create your views here.

@login_required
@permission_required('reconocimiento_deportivo.add_reconocimientodeportivo')
def solicitar(request, reconocimiento_id = None):
    """
    Abril 9, 2016
    Autor: Karent Narvaez

    Permite crear una solicitud de reconocimiento deportivo con sus datos basicos
    """
    try:
        reconocimiento = ReconocimientoDeportivo.objects.get(id=reconocimiento_id)
    except Exception:
        reconocimiento = None

    if reconocimiento:
        validado, mensaje = validar_creacion(request, reconocimiento) #Válida si no hay otra solicitud en espera de respuesta o si ya fue finalizada la solicitud que se intenta acceder
    else:
        validado = True
        mensaje = ''
    if validado:
        form = ReconocimientoDeportivoForm(instance = reconocimiento)

        if request.method == 'POST':
            form = ReconocimientoDeportivoForm(request.POST, instance = reconocimiento)

            if form.is_valid():
                nueva_solicitud = form.save(commit = False)
                nueva_solicitud.fecha_creacion = datetime.now()
                nueva_solicitud.save()
                request.session['identidad'] = {
                    'id_solicitud': nueva_solicitud.id,
                    'id_entidad': request.tenant.id,
                    'estado': True
                }
                return redirect('adjuntar_requerimientos_reconocimiento', nueva_solicitud.id)

        return render(request,'wizard/wizard_reconocimiento.html',{
            'form': form,
            'wizard_stage': 1
        })
    else:
        messages.error(request, mensaje)
        return redirect('listar_reconocimientos')


def validar_creacion(request, reconocimiento):

    mensaje = ''
    fecha_reconocimiento_actual = request.tenant.obtenerTenant().fecha_vigencia
    fecha_maxima_renovacion = date(fecha_reconocimiento_actual.year, fecha_reconocimiento_actual.month - 1, fecha_reconocimiento_actual.day%28)
    
    try:
        cantidad_solicitudes_por_respuesta = len(ReconocimientoDeportivo.objects.filter(estado = 0))
        if cantidad_solicitudes_por_respuesta > 0:
            mensaje = 'No puede crear otra solicitud mientras tenga una en espera de respuesta. Si desea crear otra debe cancelarla o esperar que sea contestada.'
            return False, mensaje
        elif  date.today() < fecha_maxima_renovacion:
            mensaje = 'No puede crear otra solicitud mientras tenga reconocimiento deportivo vigente con más de 1 mes.'
            return False, mensaje
    except:
        pass

    if reconocimiento:
        if reconocimiento.estado == 1:
            return True, mensaje
        else:
            mensaje = 'La solicitud no se puede editar porque ya fue completada.'
            return False, mensaje


@login_required
@permission_required('reconocimiento_deportivo.add_reconocimientodeportivo')
def anular_solicitud(request, reconocimiento_id = None):
    """
    Abril 9, 2016
    Autor: Karent Narvaez

    Permite cancelar una solicitud al momento de estarse creando o luego de estar creada
    :param request:
    :param reconocimiento_id:
    :return:
    """
    entidad = request.tenant
    if reconocimiento_id:
        try:
            solicitud = ReconocimientoDeportivo.objects.get(id = reconocimiento_id)
            solicitud.estado = 4
            solicitud.save()
            # Eliminar solicitud en el modelo de la entidad que lo tramitaría
            connection.set_tenant(solicitud.para_quien) #se cambia al tenant del ente tramitaría la solicitud
            solicitud_ente = ListaSolicitudesReconocimiento.objects.get(solicitud = solicitud.id, entidad_solicitante = entidad)
            solicitud_ente.delete()
            connection.set_tenant(entidad) # se retorna al tenant que realizó solicitud
        except Exception:
            messages.error(request,'No existe la solicitud, proceso no realizado')  
            
    try:
        del request.session['identidad']
    except Exception:
        pass

    messages.warning(request,'Solicitud cancelada correctamente')
    return redirect('listar_reconocimientos')


@login_required
@permission_required('reconocimiento_deportivo.view_reconocimientodeportivo')
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
        'solicitudes': solicitudes,
        'club': request.tenant.obtenerTenant()
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
def imprimir_solicitud(request, reconocimiento_id):
    """
    Abril 9, 2016
    Autor: Karent Narvaez

    Permite renderizar el html imprimible de la solicitud

    """
    try:
        solicitud = ReconocimientoDeportivo.objects.get(id = reconocimiento_id)
    except:
        messages.error(request,'No existe la solicitud')
        return redirect('listar_reconocimientos')

    solicitud.codigo_unico = solicitud.codigo_unico(request.tenant)
    discusiones = DiscusionReconocimiento.objects.filter(solicitud = solicitud)

    return render(request,'imprimir_reconocimiento.html',{
        'solicitud' : solicitud,
        'discusiones' : discusiones
    })


@login_required
@permission_required('reconocimiento_deportivo.add_reconocimientodeportivo')
def adjuntar_requerimientos(request, reconocimiento_id):
    """
    Abril 12,2016
    Autor: Karent Narvaez

    Permite adjuntar archivos  de los requerimientos a las solicitudes de reconocimiento deportivo que estan en actual creacion. se verifica la autenticidad de la peticion
    :param reconocimiento_id: id de la solicitud a la que se van a adjuntar archivos
    """
    try:
        solicitud = ReconocimientoDeportivo.objects.get(id = reconocimiento_id)
    except:
        messages.error(request,'Solicitud no encontrada')
        return redirect('listar_solicitudes')
    
    validado = validar_creacion(request, solicitud)

    if validado:
        #inicializaciones    
        cantidad_maxima_adjuntos = False
        adjuntos = solicitud.adjuntos()
        cantidad_adjuntos = solicitud.cantidad_adjuntos()
        form = AdjuntoRequerimientoReconocimientoForm(reconocimiento_id)

        #Se verifica la autenticidad de la solicitud
        try:
            auth = request.session['identidad']
            if not auth['estado'] or auth['id_solicitud'] != int(reconocimiento_id) or auth['id_entidad'] != request.tenant.id:
                raise Exception
        except Exception:
            messages.error(request,'Estas intentando editar una solicitud que ya fue completada.')
            return redirect('listar_reconocimientos')

        if cantidad_adjuntos == 16: #Si la cantidad máxima de archivos es 16 se configura un boolean en True para renderizar cierto contenido en la plantilla
            cantidad_maxima_adjuntos = True

        if request.method == 'POST':
            form = AdjuntoRequerimientoReconocimientoForm(reconocimiento_id, request.POST, request.FILES)

            if form.is_valid() and cantidad_adjuntos < 16: #Se valida que la cantidad de archivos sea máximo 16 ya que es la cantidad de archivos que se deben adjuntar de los requerimientos           
                adjunto = form.save(commit=False)
                adjunto.solicitud = solicitud
                adjunto.save()
                return redirect('adjuntar_requerimientos_reconocimiento', solicitud.id)

        return render(request,'wizard/wizard_adjuntos.html',{
            'form' : form,
            'reconocimiento_id': reconocimiento_id,
            'wizard_stage': 2,
            'adjuntos': adjuntos,
            'cantidad_maxima_adjuntos': cantidad_maxima_adjuntos
        })

    else:
        messages.error(request, 'La solicitud no se puede editar porque ya fue completada.')
        return redirect('listar_reconocimientos')


@login_required
@permission_required('reconocimiento_deportivo.add_reconocimientodeportivo')
def borrar_adjunto(request, reconocimiento_id, adjunto_id):
    """
    Abril 13, 2016
    Autor: Karent Narvaez

    Permite borrar archivos adjuntos asociados a una solicitud de reconocimiento deportivo. Se valida la autenticidad de la petición

    :param reconocimiento_id: id de la solicitud a borrar adjunto
    :param adjunto_id: id del adjunto a borrar
    """
    try:
        adjunto = AdjuntoRequerimientoReconocimiento.objects.get(id=adjunto_id, solicitud=reconocimiento_id)
    except Exception:
        messages.error(request,'No existe el archivo adjunto, no se ha realizado ninguna accion')
        return redirect('adjuntar_requerimientos_reconocimiento', reconocimiento_id)

    adjunto.delete()
    messages.success(request,'Archivo adjunto eliminado satisfactoriamente')
    return redirect('adjuntar_requerimientos_reconocimiento', reconocimiento_id)


@login_required
@permission_required('reconocimiento_deportivo.add_reconocimientodeportivo')
def finalizar_solicitud(request, solicitud_id):
    """
    Abril 13, 2016
    Autor: Karent Narvaez

    Permite guardar y completar la creacion de solicitud. 
    :param solicitud_id: id de la solicitud en creacion
    """
    entidad = request.tenant

    try:
        solicitud = ReconocimientoDeportivo.objects.get(id = solicitud_id)
        solicitud.estado = 0 #Se configura solicitud en estado 'En espera de respuesta'
        solicitud.save()
        # Crea solicitud en el modelo de la entidad que la debe tramitar
        connection.set_tenant(solicitud.para_quien) #se cambia al tenant del ente que debe tramitar solicitud
        ListaSolicitudesReconocimiento.objects.create(solicitud = solicitud.id, entidad_solicitante = entidad, fecha_creacion = datetime.now()).save()
        connection.set_tenant(entidad) # se retorna al tenant que realizó solicitud

        messages.success(request,'Solicitud enviada con éxito a:' + str(solicitud.para_quien))
        del request.session['identidad']
    except:
        messages.error(request,'Solicitud no encontrada')

    return redirect('listar_reconocimientos')


@login_required
@permission_required('reconocimiento_deportivo.add_reconocimientodeportivo')
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
    form_adjunto = AdjuntoRequerimientoReconocimientoForm(reconocimiento_id)

    return render(request,'ver_solicitud_reconocimiento.html',{
        'solicitud' : solicitud,
        'discusiones' : discusiones,
        'form_comentarios' : form,
        'form_adjunto' : form_adjunto,
        'responder' : True
    })


@login_required
@permission_required('reconocimiento_deportivo.add_reconocimientodeportivo')
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
        form_adjunto = AdjuntoRequerimientoReconocimientoForm(request.POST, request.FILESreconocimiento_id)

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

    adjuntos = AdjuntoRequerimientoReconocimiento.objects.filter(solicitud = reconocimiento_id)
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
        adjunto = AdjuntoRequerimientoReconocimiento.objects.get(solicitud = reconocimiento_id, id = adjunto_id)
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
    adjunto = AdjuntoRequerimientoReconocimiento.objects.get(solicitud = reconocimiento_id, discucion = discusion_id)
    zip,temp = comprimir_archivos(adjunto, directorio)
    response = HttpResponse(zip,content_type="application/zip")
    response['Content-Disposition'] = 'attachment; filename=adjuntos_solicitud_%s.zip'%(adjunto[0].solicitud.codigo_unico(request.tenant))
    temp.seek(0)
    response.write(temp.read())
    return response