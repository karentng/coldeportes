from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from solicitudes_escenarios.respuesta.models import ListaSolicitudes
from solicitudes_escenarios.solicitud.models import SolicitudEscenario,AdjuntoSolicitud,DiscucionSolicitud
from solicitudes_escenarios.solicitud.forms import DiscusionForm
from django.db import connection
from django.contrib import messages
from django.utils.encoding import smart_str
from solicitudes_escenarios.utilities import comprimir_archivos

# Create your views here.
@login_required
def listar_solicitudes(request):
    yo=request.tenant
    lista = ListaSolicitudes.objects.all()
    result = []
    for l in lista:
        entidad = l.entidad_solicitante
        id_sol = l.solicitud
        connection.set_tenant(entidad)
        sol = SolicitudEscenario.objects.get(id=id_sol)
        sol.entidad_solicitante = entidad
        sol.codigo = sol.codigo_unico(entidad)
        sol.escenarios_str = sol.escenarios_str()
        result.append(sol)

    connection.set_tenant(yo)
    return render(request,'lista_solicitudes.html',{
        'solicitudes': result
    })

def obtener_datos_solicitud(request,id,id_ent):
    try:
        lista = ListaSolicitudes.objects.get(entidad_solicitante=id_ent,solicitud=int(id))
    except Exception:
        messages.error(request,'No existe la solicitud')
        return False,redirect('listar_solicitudes_respuesta')

    yo = request.tenant
    entidad = lista.entidad_solicitante
    connection.set_tenant(entidad)

    solicitud = SolicitudEscenario.objects.get(id=id)
    solicitud.entidad_solicitante = entidad
    solicitud.codigo_unico = solicitud.codigo_unico(entidad)
    solicitud.escenarios_str = solicitud.escenarios_str()
    adjuntos = solicitud.adjuntos()
    array = []
    for ad in adjuntos:
        dic={
            'nombre_archivo' : ad.nombre_archivo(),
            'icon_extension' : ad.icon_extension(),
            'id' : ad.id
        }
        array.append(dic)
    solicitud.adjuntos = array

    discusiones = DiscucionSolicitud.objects.filter(solicitud=id)
    for d in discusiones:
        d.estado_actual = d.get_estado_actual_display()
        d.entidad_nombre = d.entidad.nombre
        d.tiene_adjuntos = d.tiene_adjuntos()
    discusiones = [d.__dict__ for d in discusiones]
    connection.set_tenant(yo)

    return solicitud,discusiones

@login_required
def imprimir_solicitud(request,id,id_ent):
    """
    Marzo 1, 2016
    Autor: Daniel Correa

    Permite renderizar el html imprimible de la solicitud

    """
    solicitud,discusiones = obtener_datos_solicitud(request,id,id_ent)

    if not solicitud:
        return discusiones

    return render(request,'solicitud_imprimir_respuesta.html',{
        'solicitud' : solicitud,
        'discusiones' : discusiones
    })

def ver_solicitud(request,id,id_ent):
    """
    Marzo 1, 2016
    Autor: Daniel Correa

    Permite tener el detalle de una solicitud recibida

    """
    solicitud,discusiones = obtener_datos_solicitud(request,id,id_ent)

    if not solicitud:
        return discusiones

    return render(request,'ver_solicitud_respuesta.html',{
        'solicitud' : solicitud,
        'discusiones' : discusiones,
        'responder' : False

    })

def descargar_adjunto(request,id_sol,id_adj,id_ent):
    """
    Marzo 1, 2016
    Autor: Daniel Correa

    Permite descargar algun archivo adjunto de una solicitud recibida

    """
    try:
        lista = ListaSolicitudes.objects.get(entidad_solicitante=id_ent,solicitud=int(id_sol))
    except:
        messages.error(request,'No existe la solicitud')
        return redirect('listar_solicitudes_respuesta')

    yo = request.tenant
    entidad = lista.entidad_solicitante
    connection.set_tenant(entidad)

    try:
        adj = AdjuntoSolicitud.objects.get(solicitud=id_sol,id=id_adj)
    except:
        messages.error(request,'No existe el archivo adjunto solicitado')
        return redirect('listar_solicitudes_respuesta')

    response = HttpResponse(adj.archivo.read(),content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(adj.nombre_archivo())
    response['X-Sendfile'] = smart_str(adj.archivo)

    connection.set_tenant(yo)
    return response

@login_required
def responder_solicitud(request,id,id_ent):
    """
    Marzo 2, 2016
    Autor:Daniel Correa

    Permite cargar la plantilla de respuestas de solicitudes

    """
    solicitud,discusiones = obtener_datos_solicitud(request,id,id_ent)

    if not solicitud:
        return discusiones

    form = DiscusionForm()
    return render(request,'ver_solicitud_respuesta.html',{
        'solicitud' : solicitud,
        'discusiones': discusiones,
        'form_comentarios' : form,
        'responder' : True
    })

@login_required
def enviar_respuesta(request,id,id_ent):
    """
    Marzo 2, 2016
    Autor: Daniel Correa

    Permite enviar la respuesta de una solicitud
    """
    if request.method == 'POST':

        try:
            lista = ListaSolicitudes.objects.get(entidad_solicitante=id_ent,solicitud=int(id))
        except:
            messages.error(request,'No existe la solcitud')
            return redirect('listar_solicitudes_respuesta')

        yo = request.tenant
        entidad = lista.entidad_solicitante
        connection.set_tenant(entidad)
        solicitud = SolicitudEscenario.objects.get(id=id)
        form = DiscusionForm(request.POST)
        if form.is_valid():
            dis = form.save(commit=False)
            dis.solicitud = solicitud
            dis.estado_anterior = solicitud.estado
            dis.entidad = yo
            dis.respuesta = True
            dis.save()
            for afile in request.FILES.getlist('adjuntos'):
                 AdjuntoSolicitud(solicitud = solicitud,archivo=afile,discucion = dis).save()
            solicitud.estado = dis.estado_actual
            solicitud.save()
            connection.set_tenant(yo)
            messages.success(request,'Su respuesta ha sido enviada con exito')
            return redirect('ver_solicitud_respuesta',solicitud.id,entidad.id)

        connection.set_tenant(yo)
        messages.error(request,'Tu respuesta no se ha podido enviar por un error en el formulario, intenta de nuevo')
        return redirect('responder_solicitud',solicitud.id,entidad.id)

def descargar_todos_adjuntos(request,id_sol,id_ent):
    """
    Marzo 6, 2016
    Autor: Daniel Correa

    Permite descargar todos los adjuntos de una solicitud en un archivo zip

    """
    try:
        lista = ListaSolicitudes.objects.get(entidad_solicitante=id_ent,solicitud=int(id_sol))
    except:
        messages.error(request,'No existe la solicitud')
        return redirect('listar_solicitudes_respuesta')

    yo = request.tenant
    entidad = lista.entidad_solicitante
    connection.set_tenant(entidad)

    adj = AdjuntoSolicitud.objects.filter(solicitud=id_sol)
    zip,temp = comprimir_archivos(adj)

    response = HttpResponse(zip,content_type="application/zip")
    response['Content-Disposition'] = 'attachment; filename=adjuntos_solicitud_%s.zip'%(adj[0].solicitud.codigo_unico(entidad))
    temp.seek(0)
    response.write(temp.read())
    connection.set_tenant(yo)

    return response

def descargar_adjuntos_respuesta(request,id_sol,id_ent,id_dis):
    """
    Marzo 11, 2016
    Autor: Daniel Correa

    Permite descargar los archivos adjuntos de una respuesta a una solicitud
    """
    try:
        lista = ListaSolicitudes.objects.get(entidad_solicitante=id_ent,solicitud=int(id_sol))
    except:
        messages.error(request,'No existe la solicitud')
        return redirect('listar_solicitudes_respuesta')

    yo = request.tenant
    entidad = lista.entidad_solicitante
    connection.set_tenant(entidad)

    adj = AdjuntoSolicitud.objects.filter(solicitud=id_sol, discucion=id_dis)
    zip,temp = comprimir_archivos(adj)

    response = HttpResponse(zip,content_type="application/zip")
    response['Content-Disposition'] = 'attachment; filename=adjuntos_solicitud_%s.zip'%(adj[0].solicitud.codigo_unico(entidad))
    temp.seek(0)
    response.write(temp.read())
    connection.set_tenant(yo)

    return response