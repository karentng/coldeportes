from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from solicitudes_escenarios.respuesta.models import ListaSolicitudes
from solicitudes_escenarios.solicitud.models import SolicitudEscenario,AdjuntoSolicitud
from django.db import connection
from django.contrib import messages
from django.utils.encoding import smart_str

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

@login_required
def imprimir_solicitud(request,id):
    """
    Marzo 1, 2016
    Autor: Daniel Correa

    Permite renderizar el html imprimible de la solicitud

    """
    try:

        solicitud = SolicitudEscenario.objects.get(id=id)
    except:
        messages.error(request,'No existe la solicitud')
        return redirect('listar_solicitudes')

    solicitud.codigo_unico = solicitud.codigo_unico(request.tenant)

    return render(request,'solicitud_imprimir.html',{
        'solicitud' : solicitud
    })

def ver_solicitud(request,id,id_ent):
    """
    Marzo 1, 2016
    Autor: Daniel Correa

    Permite tener el detalle de una solicitud recibida

    """
    try:
        lista = ListaSolicitudes.objects.get(entidad_solicitante=id_ent,solicitud=int(id))
    except:
        messages.error(request,'No existe la solicitud')
        return redirect('listar_solicitudes')

    yo = request.tenant
    entidad = lista.entidad_solicitante
    connection.set_tenant(entidad)

    solicitud = SolicitudEscenario.objects.get(id=id)
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

    connection.set_tenant(yo)

    return render(request,'ver_solicitud.html',{
        'solicitud' : solicitud
    })

def descargar_adjunto(request,id_sol,id_adj):
    """
    Marzo 1, 2016
    Autor: Daniel Correa

    Permite descargar algun archivo adjunto de una solicitud recibida

    """
    try:
        adj = AdjuntoSolicitud.objects.get(solicitud=id_sol,id=id_adj)
    except:
        messages.error(request,'No existe el archivo adjunto solicitado')
        return redirect('listar_solicitudes')

    response = HttpResponse(adj.archivo.read(),content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(adj.nombre_archivo())
    response['X-Sendfile'] = smart_str(adj.archivo)
    return response