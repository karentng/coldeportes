from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from solicitudes_escenarios.respuesta.models import ListaSolicitudes
from solicitudes_escenarios.solicitud.models import SolicitudEscenario
from django.db import connection
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