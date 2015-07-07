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


@login_required
def listar_escenarios_ccfs(request):
    """
    Julio 5 / 2015
    Autor: Karent Narvaez Grisales
    
    listar los escenarios de las CCF del tenant respectivo

    Se obtienen los escenario que ha registrado el tenant que realiza la petición

    :param request:   Petición realizada
    :type request:    WSGIRequest
    """
    ccfs = CajaCompensacion.objects.all()
    return render(request, 'cajas_compensacion/escenarios_ccf_lista.html', {
        'ccfs': ccfs,
    })

@login_required
def finalizar_escenario_ccf(request):
    """
    Julio 5 / 2015
    Autor: Karent Narvaez Grisales
    
    enviar mensaje de finalizada la creación de escenario CCF


    :param request:   Petición realizada
    :type request:    WSGIRequest
    """
    messages.success(request, "Escenario CCF registrado correctamente.")
    
    return redirect('listar_escenarios_ccfs')

@login_required
def desactivar_escenario_ccf(request, ccf_id):
    """
    Julio 5 / 2015
    Autor: Karent Narvaez Grisales
    
    desactivar escenario de caja de compensación

    Se obtienen el estado actual del escenario CCF y se invierte.

    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param escenario_id:   Identificador del escenario
    :type escenario_id:    String
    """
    ccf = CajaCompensacion.objects.get(id=ccf_id)
    estado_actual = ccf.activo
    ccf.activo = not(estado_actual)
    ccf.save()
    messages.warning(request, "Escenario CCF cambiado de estado correctamente.")
    return redirect('listar_escenarios_ccfs')

@login_required
def ver_escenario_ccf(request, ccf_id):
    """
    Julio 5 / 2015
    Autor: Karent Narvaez Grisales
    
    ver escenario de cafas de compensación

    Se obtienen toda la información registrada del escenario de la caja de compensación dado y se muestra.

    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param ccf_id:   Identificador del escenario
    :type ccf_id:    String
    """
    escenario_ccf = CajaCompensacion.objects.get(id=ccf_id)
    horarios = HorarioDisponibilidadCajas.objects.filter(caja_compensacion=ccf_id)
    tarifas = Tarifa.objects.filter(caja_compensacion=ccf_id)
    contactos = ContactoCajas.objects.filter(caja_compensacion=ccf_id)

    return render(request, 'cajas_compensacion/ver_escenario_ccf.html', {
        'escenario_ccf': escenario_ccf,
        'horarios': horarios,
        'tarifas': tarifas,
        'contactos': contactos
    })

@login_required
def wizard_caja_escenario(request):
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
        'titulo': 'Identificación del Escenario CCF',
        'wizard_stage': 1,
        'form': caja_form,
    })

@login_required
def wizard_editar_caja_escenario(request, caja_id):
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
        'titulo': 'Identificación del Caja de Compensación',
        'wizard_stage': 1,
        'form': caja_form,
    })


@login_required
def wizard_horarios_ccf(request, ccf_id):
    """
    Julio 5 / 2015
    Autor: Karent Narvaez Grisales
    
    Horarios de disponibilidad de un escenario de caja de compensacion

    Se obtienen el formulario de los horarios y se muestran los horarios actualmente añadidos al escenario
    y si hay modificaciones se guardan.
    Si el escenario es nuevo se inicializa en nulo.

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
        'titulo': 'Horarios de Disponibilidad del Escenario CCF',
        'wizard_stage': 2,
        'form': horarios_form,
        'horarios': horarios,
        'ccf_id': ccf_id
    })



@login_required
def wizard_contactos_ccf(request, ccf_id):
    """
    Julio 5 / 2015
    Autor: Karent Narvaez Grisales
    
    Contactos de un escenario de caja de compensación

    Se obtienen el formulario para subir contactos y se muestran los que actualmente hay añadidos al escenario
    y si hay modificaciones se guardan.
    Si el escenario es nuevo se inicializa en nulo.

    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param ccf_id:   Identificador del escenario
    :type ccf_id:    String
    """

    try:
        contactos = ContactoCajas.objects.filter(caja_compensacion=ccf_id)
    except Exception:
        contactos = None

    contactos_form = ContactoCajasForm()

    if request.method == 'POST':
        contactos_form = ContactoCajasForm(request.POST)

        if contactos_form.is_valid():
            contacto_nuevo = contactos_form.save(commit=False)
            contacto_nuevo.caja_compensacion = CajaCompensacion.objects.get(id=ccf_id)
            contacto_nuevo.nombre = contacto_nuevo.nombre.upper()
            contacto_nuevo.save()
            #messages.success(request, "¡Escenario guardado exitósamente!")
            return redirect('wizard_contactos_ccf', ccf_id)


    return render(request, 'cajas_compensacion/wizard/wizard_4.html', {
        'titulo': 'Contactos del Escenario CCF',
        'wizard_stage': 4,
        'form': contactos_form,
        'contactos': contactos,
        'ccf_id': ccf_id
    })

@login_required
def wizard_tarifas_ccf(request, ccf_id):
    """
    Julio 5 / 2015
    Autor: Karent Narvaez Grisales
    
    Tarifas de un escenario de caja de compensación

    Se obtienen el formulario para crear tarifas y se muestran las que actualmente hay añadidas al escenario CCF
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
        'titulo': 'Tarifas del Escenario CCF',
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
    
    Eliminar horario de un escenario de caja de compensación

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
def eliminar_contacto_ccf(request, ccf_id, contacto_id):
    """
    Julio 5 / 2015
    Autor: Karent Narvaez Grisales
    
    Eliminar contacto de Caja de Compensación

    Se obtienen el contacto de la base de datos y se elimina

    :param request:   Petición realizada
    :type request:    WSGIRequest
    :param ccf_id:   Identificador del escenario
    :type ccf_id:    String
    :param contacto_id:   Identificador del contacto
    :type contacto_id:    String
    """

    try:
        contacto = ContactoCajas.objects.get(id=contacto_id, caja_compensacion=ccf_id)
        contacto.delete()
        return redirect('wizard_contactos_ccf', ccf_id)
    except Exception:
        return redirect('wizard_contactos_ccf', ccf_id)


@login_required
def eliminar_tarifa_ccf(request, ccf_id, tarifa_id):
    """
    Julio 5 / 2015
    Autor: Karent Narvaez Grisales
    
    Eliminar contacto de Caja de Compensación

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


