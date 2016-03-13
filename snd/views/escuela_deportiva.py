from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.db import connection
from snd.formularios.escuela_deportiva  import *
from snd.models import *
from entidades.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from coldeportes.utilities import *

#==================================================================
# Crear / Modificar Escuela de formación deportiva
#==================================================================

"""
Noviembre 02 / 2015
Autor: Cristian Leonardo Ríos López

Diccionario con los formularios, # de paso, paso anterior, paso siguiente y plantilla del wizard
"""
ESCUELA_DEPORTIVA_WIZARD = {
    "identificacion": [EscuelaDeportivaForm, 1, None, "servicios", "escuela_deportiva/wizard/escuela_deportiva_identificacion.html"],
    "servicios": [EscuelaDeportivaServiciosForm, 2, "identificacion", None, "escuela_deportiva/wizard/escuela_deportiva_servicios.html"],
}

@login_required
@all_permission_required('snd.add_escueladeportiva')
def obtenerDatosPasoDelWizard(request, paso):
    """
    Noviembre 02 / 2015
    Autor: Cristian Leonardo Ríos López

    Retorna los datos del paso del wizard que recibe

    Retorno el valor del diccionario que se recibe como parámetro

    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param paso:      Paso actual del Wizard
    :type paso:       String
    :returns:         Lista con los datos del Wizard
    :rtype:           List
    """
    return ESCUELA_DEPORTIVA_WIZARD[paso]


@login_required
@all_permission_required('snd.add_escueladeportiva')
def crear_editar(request,paso,edicion,escuela_deportiva_id=None):
    """
    Noviembre 02 / 2015
    Autor: Cristian Leonardo Ríos López
    
    Crear una Escuela de Formación Deportiva

    Se obtienen los formularios de información de la escuela de formación deportiva con los datos diligenciados y se guardan.

    :param request:   Petición realizada
    :type request:    WSGIRequest
    """

    form, paso_wizard, anterior, siguiente, plantilla = obtenerDatosPasoDelWizard(request, paso)

    try:
        escuela_deportiva = EscuelaDeportiva.objects.get(id=escuela_deportiva_id)
    except EscuelaDeportiva.DoesNotExist:
        if escuela_deportiva_id == None:
            escuela_deportiva = None
        else:
            messages.error(request, "Está tratando de editar una Escuala de Formación Deportiva inexistente.")
            return redirect('escuela_deportiva_listar')


    if request.method == 'POST':
        form = form(request.POST, request.FILES, instance=escuela_deportiva)
        if form.is_valid():
            escuela_deportiva = form.save(commit=False)
            escuela_deportiva.entidad = request.tenant
            escuela_deportiva.save()
            form.save_m2m()
            if siguiente == None:
                return finalizar(request,opcion='listar',edicion=edicion)
            else:
                return redirect('escuela_deportiva_crear_editar', paso=siguiente, escuela_deportiva_id=escuela_deportiva.id, edicion=edicion)

    form = form(instance=escuela_deportiva)

    return render(request, plantilla, {
        'wizard_stage': paso_wizard,
        'anterior': anterior,
        'escuela_deportiva_id': escuela_deportiva_id,
        'edicion': edicion,
        'form': form,
    })

@login_required
@all_permission_required('snd.add_escueladeportiva')
def finalizar(request, opcion, edicion):
    """
    Noviembre 02 / 2015
    Autor: Cristian Leonardo Ríos López
    
    enviar mensaje de finalizada la creación de la escuela de formación deportiva


    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param opcion: indica si se quiere ir a listar o a registrar una escuela de formación deportiva
    :type opcion: String
    :param edicion: indica si se está editando una escuela de formación deportiva existente o si se está registrando una escuela de formación deportiva nueva
    :type edicion: Integer
    """

    if edicion == 0 or edicion == '0':
        messages.success(request, "Escual de Formación Deportiva registrada correctamente.")
    else:
        messages.success(request, "Escuela de Formación Deportiva editada correctamente.")

    if opcion == "nuevo":
        return redirect('escuela_deportiva_crear_editar',paso=identificacion,edicion=0)
    elif opcion == "listar":
        return redirect('escuela_deportiva_listar')

@login_required
@all_permission_required('snd.view_escueladeportiva')
def ver(request,escuela_deportiva_id,id_entidad):
    """
    Noviembre 02 / 2015
    Autor: Cristian Leonardo Ríos López
    
    ver escuela de formación deportiva

    Se obtienen toda la información registrada de la escual de formación deportiva dada y se muestra.

    Se pide la entidad para conectarse y obtener la información de un objeto
    desde la entidad correcta, esto para efectos de consulta desde otro ente cuando sea necesario.

    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param escuela_deportiva_id:   Identificador de la escuela de formación deportiva
    :type escuela_deportiva_id:    String
    :param id_entidad: Llave primaria de la entidad a la que pertenece la escuela de formación deportiva
    :type id_entidad: String
    """
    tenant = Entidad.objects.get(id=id_entidad).obtenerTenant()
    connection.set_tenant(tenant)
    ContentType.objects.clear_cache()
    try:
        escuela_deportiva = EscuelaDeportiva.objects.get(id=escuela_deportiva_id)
    except EscuelaDeportiva.DoesNotExist:
        messages.error(request, 'La escuela deportiva que desea ver no existe')
        return redirect('escuela_deportiva_listar')

    return render(request, 'escuela_deportiva/escuela_deportiva_ver.html', {
        'escuela': escuela_deportiva
    })

@login_required
@all_permission_required('snd.view_escueladeportiva')
def listar(request):
    """
    Noviembre 02 / 2015
    Autor: Cristian Leonardo Ríos López
    
    listar las escuelas de formación deportiva de la respectiva entidad

    Se pasa el tipo de tenant para que se haga la carga respectiva de datos

    :param request:   Petición realizada
    :type request:    WSGIRequest
    """
    return render(request, 'escuela_deportiva/escuela_deportiva_lista.html', {
        'tipo_tenant':request.tenant.tipo
    })


@login_required
@permission_required('snd.change_escueladeportiva')
def desactivar_escuela_deportiva(request,id_escuela):
    """
    Junio 9 / 2015
    Autor: Milton Lenis

    Cambiar estado de una escuela deportiva

    Se obtiene el estado actual y se invierte su valor

    :param request: Petición Realizada
    :type request: WSGIRequest
    :param id_escuela: Llave primaria de la escuela
    :type id_escuela: String
    """
    try:
        escuela = EscuelaDeportiva.objects.get(id=id_escuela)
    except:
        messages.error(request, "La escuela que está intentando desactivar no existe")
        return redirect('escuela_deportiva_listar')

    estado_actual = escuela.estado
    escuela.estado = not(estado_actual)
    escuela.save()
    if(estado_actual):
        message = "Escuela deportiva activada correctamente."
    else:
        message = "Escuela deportiva desactivada correctamente."
    messages.success(request, message)
    return redirect('escuela_deportiva_listar')
