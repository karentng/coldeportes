from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.db import connection
from snd.formularios.centro_biomedico  import *
from snd.models import *
from entidades.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from coldeportes.utilities import *

#==================================================================
# Crear / Modificar Centro Biomédico
#==================================================================

"""
Octubre 03 / 2015
Autor: Cristian Leonardo Ríos López

Diccionario con los formularios, # de paso, paso anterior, paso siguiente y plantilla del wizard
"""
CENTRO_BIOMEDICO_WIZARD = {
    "identificacion": [CentroBiomedicoForm, 1, None, "servicios", "centro_biomedico/wizard/centro_biomedico_identificacion.html"],
    "servicios": [CentroBiomedicoServiciosForm, 2, "identificacion", None, "centro_biomedico/wizard/centro_biomedico_servicios.html"],
}

@login_required
@all_permission_required('snd.add_centrobiomedico')
def obtenerDatosPasoDelWizard(request, paso):
    """
    Octubre 03 / 2015
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
    return CENTRO_BIOMEDICO_WIZARD[paso]


@login_required
@all_permission_required('snd.add_centrobiomedico')
def crear_editar(request,paso,edicion,centro_biomedico_id=None):
    """
    Octubre 03 / 2015
    Autor: Cristian Leonardo Ríos López
    
    Crear un Centro Biomédico

    Se obtienen los formularios de información del centro biomédico con los datos diligenciados y se guardan.

    :param request:   Petición realizada
    :type request:    WSGIRequest
    """

    form, paso_wizard, anterior, siguiente, plantilla = obtenerDatosPasoDelWizard(request, paso)

    try:
        centro_biomedico = CentroBiomedico.objects.get(id=centro_biomedico_id)
    except CentroBiomedico.DoesNotExist:
        if centro_biomedico_id == None:
            centro_biomedico = None
        else:
            messages.error(request, "Está tratando de editar un centro biomédico inexistente.")
            return redirect('centro_biomedico_listar')


    if request.method == 'POST':
        form = form(request.POST, instance=centro_biomedico)
        if form.is_valid():
            centro_biomedico = form.save(commit=False)
            centro_biomedico.entidad = request.tenant
            centro_biomedico.save()
            form.save_m2m()
            if siguiente == None:
                return finalizar(request,opcion='listar',edicion=edicion)
            else:
                return redirect('centro_biomedico_crear_editar', paso=siguiente, centro_biomedico_id=centro_biomedico.id, edicion=edicion)

    form = form(instance=centro_biomedico)

    return render(request, plantilla, {
        'wizard_stage': paso_wizard,
        'anterior': anterior,
        'centro_biomedico_id': centro_biomedico_id,
        'edicion': edicion,
        'form': form,
    })

@login_required
@all_permission_required('snd.add_centrobiomedico')
def finalizar(request, opcion, edicion):
    """
    Octubre 04 / 2015
    Autor: Cristian Leonardo Ríos López
    
    enviar mensaje de finalizada la creación del centro biomédico


    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param opcion: indica si se quiere ir a listar o a registrar un centro biomédico nuevo
    :type opcion: String
    :param edicion: indica si se está editando un centro biomédico existente o si se está registrando un centtro biomédico nuevo
    :type edicion: Integer
    """

    if edicion == 0 or edicion == '0':
        messages.success(request, "Centro Biomédico registrado correctamente.")
    else:
        messages.success(request, "Centro Biomédico editado correctamente.")

    if opcion == "nuevo":
        return redirect('centro_biomedico_crear_editar',paso=identificacion,edicion=0)
    elif opcion == "listar":
        return redirect('centro_biomedico_listar')

@login_required
@all_permission_required('snd.view_centrobiomedico')
def ver(request,centro_biomedico_id,id_entidad):
    """
    Octubre 10 / 2015
    Autor: Cristian Leonardo Ríos López
    
    ver centro biomédico

    Se obtienen toda la información registrada del centro biomédico dado y se muestra.

    Se pide la entidad para conectarse y obtener la información de un objeto
    desde la entidad correcta, esto para efectos de consulta desde otro ente cuando sea necesario.

    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param centro_biomedico_id:   Identificador del centro biomedico
    :type centro_biomedico_id:    String
    :param id_entidad: Llave primaria de la entidad a la que pertenece el centro biomedico
    :type id_entidad: String
    """
    tenant = Entidad.objects.get(id=id_entidad).obtenerTenant()
    connection.set_tenant(tenant)
    ContentType.objects.clear_cache()
    try:
        centro_biomedico = CentroBiomedico.objects.get(id=centro_biomedico_id)
    except CentroBiomedico.DoesNotExist:
        messages.error(request, 'El centro biomédico que desea ver no existe')
        return redirect('centro_biomedico_listar')

    return render(request, 'centro_biomedico/centro_biomedico_ver.html', {
        'centro': centro_biomedico
    })

@login_required
@all_permission_required('snd.view_centrobiomedico')
def listar(request):
    """
    Octubre 04 / 2015
    Autor: Cristian Leonardo Ríos López
    
    listar los centros biomédicos de la respectiva entidad

    Se pasa el tipo de tenant para que se haga la carga respectiva de datos

    :param request:   Petición realizada
    :type request:    WSGIRequest
    """
    return render(request, 'centro_biomedico/centro_biomedico_lista.html', {
        'tipo_tenant':request.tenant.tipo
    })