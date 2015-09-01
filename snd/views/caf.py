from django.contrib.contenttypes.models import ContentType
from django.db import connection
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from formtools.wizard.views import *
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from snd.models import *
from entidades.models import *
from snd.formularios.caf import *
from django.contrib import messages
from coldeportes.utilities import *

#==================================================================
# Crear / Modificar CAF
#==================================================================

"""
Julio 09 / 2015
Autor: Andrés Serna

Diccionario con los formularios, # de paso, paso anterior, paso siguiente y plantilla del wizard
"""
CAF_WIZARD = {
    "Identificación": [CentroAcondicionamientoForm, 1, None, "Planes", "cafs/wizard/cafs_crear.html"],
    "Planes": [CAPlanForm, 2, "Identificación", "Clases", "cafs/wizard/cafs_crear_planes.html"],
    "Clases": [CAClasesForm, 3, "Planes", "Servicios", "cafs/wizard/cafs_crear_clases.html"],
    "Servicios": [CAServiciosForm, 4, "Clases", "Fotos", "cafs/wizard/cafs_crear_servicios.html"],
    "Fotos": [CAFotoForm, 5, "Servicios", None, "cafs/wizard/cafs_crear_fotos.html"],
}

@login_required
@all_permission_required('snd.add_centroacondicionamiento')
def obtenerDatosPasoDelWizard(request, paso):
    """
    Julio 09 / 2015
    Autor: Andrés Serna

    Retorna los datos del paso del wizard que recibe

    Retorno el valor del diccionario que se recibe como parámetro

    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param paso:      Paso actual del Wizard
    :type paso:       String
    :returns:         Lista con los datos del Wizard
    :rtype:           List
    """
    return CAF_WIZARD[paso]

@login_required
@all_permission_required('snd.add_centroacondicionamiento')
def crear(request, paso, idCAF=None):
    """
    Julio 09 / 2015
    Autor: Andrés Serna

    Maneja el Wizard de Creación y Modificacion de CAF

    Obtengo los datos del paso actual del Wizard, el cual recibo como parámetro y renderizo los datos en su respectivo HTML

    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param paso:      Paso actual del Wizard
    :type paso:       String
    :param idCAF:     Identificador del CAF que se esta modificando
    :type idCAF:      String
    """

    form, paso_wizard, anterior, siguiente, plantilla = obtenerDatosPasoDelWizard(request, paso)

    try:
        centro = CentroAcondicionamiento.objects.get(id=idCAF)
    except Exception:
        if idCAF == None:
            centro = None
        else:
            return redirect('listar_cafs')

    if request.method == 'POST':
        form = form(request.POST, instance=centro)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.entidad = request.tenant
            obj.save()
            form.save_m2m()
            return redirect('crear_caf', paso=siguiente, idCAF=obj.id)
    else:
        if paso != "Planes":
            form = form(instance=centro)

    planes = CAPlan.objects.filter(centro=centro)
    fotos = CAFoto.objects.filter(centro=centro)

    return render(request, plantilla, {
        'paso_wizard': paso_wizard,
        'anterior': anterior,
        'planes': planes,
        'fotos': fotos,
        'idCAF': idCAF,
        'form': form,
    })

@login_required
@all_permission_required('snd.add_centroacondicionamiento')
def finalizar(request, otroCAF):
    """
    Julio 09 / 2015
    Autor: Andrés Serna

    Finaliza el proceso de creación / modificación de CAF

    Envio el mensaje de registro finalizado, y redirecciono a crear un nuevo CAF o listar los CAF, según haya elegido el usuario

    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param otroCAF:   1. Crear otro CAF 0. Listar CAF existentes
    :type otroCAF:    String
    """
    messages.success(request, "Centro de acondicionamiento registrado correctamente.")
    if otroCAF == '1':
        return redirect('crear_caf', 'Identificación')
    
    return redirect('listar_cafs')

#==================================
# Crear / Eliminar Planes del CAF
#==================================

@login_required
@all_permission_required('snd.add_centroacondicionamiento')
def crear_plan(request, idCAF):
    """
    Julio 09 / 2015
    Autor: Andrés Serna

    Crea un plan del CAF

    Obtengo los datos del formulario enviados por POST y guardo el plan si el formulario es válido

    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param idCAF:     Identificador del CAF al cual se asociará el plan
    :type idCAF:      String
    """
    try:
        centro = CentroAcondicionamiento.objects.get(id=idCAF)
    except Exception:
        return redirect('listar_cafs')

    if request.method == 'POST':
        form = CAPlanForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.centro = centro
            obj.save()
        return redirect('crear_caf', paso="Planes", idCAF=idCAF)
    
    return redirect('listar_cafs')

@login_required
@all_permission_required('snd.add_centroacondicionamiento')
def eliminar_plan(request, idCAF, idPlan):
    """
    Julio 09 / 2015
    Autor: Andrés Serna
    
    Retorna el formulario elegido de acuerdo a idForm

    Elimina un plan asociado a un CAF

    Obtengo el identificador del plan a eliminar, traigo el objeto y lo elimino

    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param idCAF:     Identificador del CAF al cual se asociará el plan
    :type idCAF:      String
    :param idPlan:    Identificador del Plan el cual será eliminado
    :type idPlan:     String
    """
    try:
        centro = CentroAcondicionamiento.objects.get(id=idCAF)
    except Exception:
        return redirect('listar_cafs')

    try:
        plan = CAPlan.objects.get(id=idPlan, centro=centro)
    except Exception:
        return redirect('crear_caf', paso="Planes", idCAF=idCAF)

    plan.delete()

    return redirect('crear_caf', paso="Planes", idCAF=idCAF)

#==================================
# Crear / Eliminar Fotos del CAF
#==================================
@login_required
@all_permission_required('snd.add_centroacondicionamiento')
def crear_foto(request, idCAF):
    """
    Julio 09 / 2015
    Autor: Andrés Serna
    
    Modificar un CAF

    Registrar una foto del CAF

    Obtengo los datos del formulario enviados por POST y guardo la foto si el formulario es válido

    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param idCAF:     Identificador del CAF al cual se asociará el plan
    :type idCAF:      String
    """
    try:
        centro = CentroAcondicionamiento.objects.get(id=idCAF)
    except Exception:
        return redirect('listar_cafs')

    if request.method == 'POST':
        form = CAFotoForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.centro = centro
            obj.save()
        return redirect('crear_caf', paso="Fotos", idCAF=idCAF)
    
    return redirect('listar_cafs')

@login_required
@all_permission_required('snd.add_centroacondicionamiento')
def eliminar_foto_caf(request, idCAF, idFoto):
    """
    Julio 09 / 2015
    Autor: Andrés Serna

    Elimina una foto asociada a un CAF

    Obtengo el identificador de la foto a eliminar, traigo el objeto y lo elimino

    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param idCAF:     Identificador del CAF al cual se asociará el plan
    :type idCAF:      String
    :param idFoto:    Identificador de la foto que cual será eliminada
    :type idFoto:     String
    """
    try:
        centro = CentroAcondicionamiento.objects.get(id=idCAF)
    except Exception:
        return redirect('listar_cafs')

    try:
        foto = CAFoto.objects.get(id=idFoto)
    except Exception:
        return redirect('crear_caf', paso="Fotos", idCAF=idCAF)

    foto.delete()

    return redirect('crear_caf', paso="Fotos", idCAF=idCAF)

#==================================================================
# Listar CAF
#==================================================================

@login_required
def listarCAFS(request):
    """
    Mayo 26 / 2015
    Autor: Andrés Serna
    
    Despliega todos los CAF's registrados en la entidad

    Obtengo todos los CAF's y los envío al template como "cafs"

    :param request:   Petición realizada
    :type request:    WSGIRequest
    """
    return render(request, 'cafs/cafs_lista.html', {
        'tipo_tenant':request.tenant.tipo
    })

@login_required
def ver_caf(request, idCAF,id_entidad):
    """
    Junio 23 / 2015
    Autor: Andrés Serna
    
    Ver CAF

    Se obtienen toda la información registrada del CAF dado y se muestra.

    Edición: Septiembre 1 /2015
    NOTA: Para esta funcionalidad se empezó a pedir la entidad para conectarse y obtener la información de un objeto
    desde la entidad correcta, esto para efectos de consulta desde una liga o una federación.

    :param request:        Petición realizada
    :type request:         WSGIRequest
    :param escenario_id:   Identificador del CAF
    :type escenario_id:    String
    :param id_entidad: Llave primaria de la entidad a la que pertenece el personal de apoyo
    :type id_entidad: String
    """
    tenant = Entidad.objects.get(id=id_entidad).obtenerTenant()
    connection.set_tenant(tenant)
    ContentType.objects.clear_cache()
    try:
        centro = CentroAcondicionamiento.objects.get(id=idCAF)
        planes = CAPlan.objects.filter(centro=centro)
        fotos = CAFoto.objects.filter(centro=centro)
    except Exception:
        return redirect('listar_cafs')

    return render(request, 'cafs/ver_caf.html', {
        'centro': centro,
        'planes': planes,
        'fotos': fotos,
        'contenidoSinPadding': True,
    })

'''
@login_required
@all_permission_required('snd.change_centroacondicionamiento')
def desactivarCAF(request, idCAF):
    """
    Mayo 26 / 2015
    Autor: Andrés Serna
    
    Desactiva el CAF seleccionado

    Recupero el identificador del CAF seleccionado, lo obtengo de la base de datos, asigno la negación de su estado actual y lo guardo.

    :param wizard:   Wizard que se despliega
    :type wizard:    NamedUrlSessionWizardView
    :param idCAF:    Identificador del CAF seleccionado
    :type idCAF:     String
    """
    try:
        caf = CentroAcondicionamiento.objects.get(id=idCAF)
    except Exception:
        return redirect('listar_cafs')

    caf.activo = not(caf.activo)
    caf.save()
    
    return redirect('listar_cafs')
'''