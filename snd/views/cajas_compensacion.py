from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from formtools.wizard.views import SessionWizardView
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
import os
from snd.formularios.cajas_compensacion import *
from snd.models import *
from entidades.models import *
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist



@login_required
def listar_ccfs(request):
    """
    Julio 5 / 2015
    Autor: Karent Narvaez Grisales
    
    listar las CCF del tenant respectivo

    Se obtienen las CCF que se ha registrado en el tenant que realiza la petición

    :param request:   Petición realizada
    :type request:    WSGIRequest
    """
    ccfs = CajaCompensacion.objects.all()
    return render(request, 'cajas_compensacion/ccf_lista.html', {
        'ccfs': ccfs,
    })

@login_required
def finalizar_ccf(request, opcion):
    """
    Julio 5 / 2015
    Autor: Karent Narvaez Grisales
    
    enviar mensaje de finalizada la creación de la CCF


    :param request:   Petición realizada
    :type request:    WSGIRequest
    """
    messages.success(request, "CCF registrado correctamente.")
    if opcion=='nuevo':
        return redirect('wizard_caja')
    else:
        return redirect('listar_ccfs')

@login_required
def desactivar_ccf(request, ccf_id):
    """
    Julio 5 / 2015
    Autor: Karent Narvaez Grisales
    
    desactivar caja de compensación

    Se obtienen el estado actual del escenario CCF y se invierte.

    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param escenario_id:   Identificador del escenario
    :type escenario_id:    String
    """
    try:
        ccf = CajaCompensacion.objects.get(id=ccf_id)
    except ObjectDoesNotExist:
        messages.warning(request, "La Caja de compensación que intenta acceder no existe.")
        return redirect('listar_ccfs')

    estado_actual = ccf.activo
    ccf.activo = not(estado_actual)
    ccf.save()
    messages.warning(request, "CCF cambiada de estado correctamente.")
    return redirect('listar_ccfs')

@login_required
def ver_ccf(request, ccf_id):
    """
    Julio 5 / 2015
    Autor: Karent Narvaez Grisales
    
    ver cafas de compensación

    Se obtienen toda la información registrada de la caja de compensación dado y se muestra.

    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param ccf_id:   Identificador del escenario
    :type ccf_id:    String
    """
    try:
        ccf = CajaCompensacion.objects.get(id=ccf_id)
    except ObjectDoesNotExist:
        messages.warning(request, "La caja de compensación que intenta acceder no existe.")
        return redirect('listar_ccfs')
    horarios = HorarioDisponibilidadCajas.objects.filter(caja_compensacion=ccf_id)
    tarifas = Tarifa.objects.filter(caja_compensacion=ccf_id)

    return render(request, 'cajas_compensacion/ver_ccf.html', {
        'ccf': ccf,
        'horarios': horarios,
        'tarifas': tarifas,
    })

@login_required
def wizard_caja(request):
    """
    Julio 4 / 2015
    Autor: Karent Narvaez Grisales
    
    Registrar una caja de compensacion

    Se obtienen los formularios de información de la caja de compensacion, luego estos mismo formularios con los datos diligenciados y se guardan.

    :param request:   Petición realizada
    :type request:    WSGIRequest
    """
    caja_form = CajaCompensacionForm( )
    if request.method == 'POST':

        caja_form = CajaCompensacionForm(request.POST)

        if caja_form.is_valid():
            caja = caja_form.save(commit=False)
            caja.nombre = caja.nombre.upper()
            caja.entidad =  request.tenant
            caja.save()
            caja_form.save()
            return redirect('wizard_horarios_ccf', caja.id)
    

    return render(request, 'cajas_compensacion/wizard/wizard_1.html', {
        'titulo': 'Identificación de la CCF',
        'wizard_stage': 1,
        'form': caja_form,
    })

@login_required
def wizard_editar_caja(request, caja_id):
    """
    Julio 4 / 2015
    Autor: Karent Narvaez Grisales
    
    Editar una caja de compensación: Paso datos de identificación 

    Se obtienen los formularios de información de la caja de compensacion con los datos diligenciados y se guardan.

    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param caja_id:   Identificador del escenario
    :type caja_id:    String
    """

    try:
        caja = CajaCompensacion.objects.get(id=caja_id)
    except Exception:
        caja = None

    caja_form = CajaCompensacionForm(instance=caja)

    if request.method == 'POST':

        caja_form = CajaCompensacionForm(request.POST, instance=caja)

        if caja_form.is_valid():
            caja = caja_form.save(commit=False)
            caja.nombre = caja.nombre.upper()
            caja.save()
            caja_form.save()
            return redirect('wizard_horarios_ccf', caja.id)


    return render(request, 'cajas_compensacion/wizard/wizard_1.html', {
        'titulo': 'Identificación de la Caja de Compensación',
        'wizard_stage': 1,
        'form': caja_form,
    })


@login_required
def wizard_horarios_ccf(request, ccf_id):
    """
    Julio 5 / 2015
    Autor: Karent Narvaez Grisales
    
    Horarios de disponibilidad de una caja de compensacion

    Se obtienen el formulario de los horarios y se muestran los horarios actualmente añadidos a la caja de compensación
    y si hay modificaciones se guardan.
    Si la caja de compensación es nueva se inicializan en nulo los horarios.

    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param ccf:   Identificador del escenario CCF
    :type ccf:    String
    """

    try:
        horarios = HorarioDisponibilidadCajas.objects.filter(caja_compensacion=ccf_id)
    except Exception:
        horarios = None

    horarios_form = HorariosDisponibleCajasForm()

    if request.method == 'POST':
        horarios_form = HorariosDisponibleCajasForm(request.POST)

        if horarios_form.is_valid():
            horario_nuevo = horarios_form.save(commit=False)
            horario_nuevo.caja_compensacion = CajaCompensacion.objects.get(id=ccf_id)
            horario_nuevo.save()
            horarios_form.save()
            return redirect('wizard_horarios_ccf', ccf_id)


    return render(request, 'cajas_compensacion/wizard/wizard_2.html', {
        'titulo': 'Horarios de Disponibilidad de la CCF',
        'wizard_stage': 2,
        'form': horarios_form,
        'horarios': horarios,
        'ccf_id': ccf_id
    })

@login_required
def wizard_tarifas_ccf(request, ccf_id):
    """
    Julio 5 / 2015
    Autor: Karent Narvaez Grisales
    
    Tarifas de una caja de compensación

    Se obtienen el formulario para crear tarifas y se muestran las que actualmente hay añadidas a la CCF
    y si hay modificaciones se guardan.
    Si el escenario es nuevo se inicializa en nulo.

    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param ccf_id:   Identificador del escenario
    :type ccf_id:    String
    """

    try:
        tarifas = Tarifa.objects.filter(caja_compensacion=ccf_id)
    except Exception:
        tarifas = None

    tarifas_form = TarifaCajasForm()

    if request.method == 'POST':
        tarifas_form = TarifaCajasForm(request.POST)

        if tarifas_form.is_valid():
            tarifa_nueva = tarifas_form.save(commit=False)
            tarifa_nueva.caja_compensacion = CajaCompensacion.objects.get(id=ccf_id)
            tarifa_nueva.titulo = tarifa_nueva.titulo.upper()
            tarifa_nueva.save()
            return redirect('wizard_tarifas_ccf', ccf_id)


    return render(request, 'cajas_compensacion/wizard/wizard_3.html', {
        'titulo': 'Tarifas de la CCF',
        'wizard_stage': 3,
        'form': tarifas_form,
        'tarifas': tarifas,
        'ccf_id': ccf_id
    })


@login_required
def eliminar_horario_ccf(request, ccf_id, horario_id):
    """
    Julio 5 / 2015
    Autor: Karent Narvaez Grisales
    
    Eliminar horario de una caja de compensación

    Se obtienen el horario de la base de datos y se elimina

    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param ccf_id:   Identificador del escenario CCF
    :type ccf_id:    String
    """

    try:
        horario = HorarioDisponibilidadCajas.objects.get(id=horario_id, caja_compensacion=ccf_id)
        horario.delete()
        return redirect('wizard_horarios_ccf', ccf_id)

    except Exception:
        return redirect('wizard_horarios_ccf', ccf_id)


@login_required
def eliminar_tarifa_ccf(request, ccf_id, tarifa_id):
    """
    Julio 5 / 2015
    Autor: Karent Narvaez Grisales
    
    Eliminar tarifa de Caja de Compensación

    Se obtienen el contacto de la base de datos y se elimina

    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param ccf_id:   Identificador del escenario
    :type ccf_id:    String
    :param tarifa_id:   Identificador del contacto
    :type tarifa_id:    String
    """

    try:
        tarifa = Tarifa.objects.get(id=tarifa_id, caja_compensacion=ccf_id)
        tarifa.delete()
        return redirect('wizard_tarifas_ccf', ccf_id)
    except Exception:
        return redirect('wizard_tarifas_ccf', ccf_id)


