from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from formtools.wizard.views import SessionWizardView
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
import os
from snd.formularios.deportistas  import *
from snd.models import *
from entidades.models import *
from django.contrib import messages

@login_required
def desactivar_deportista(request):
    return redirect('/escenarios/listar')

@login_required
def listar_deportista(request):
    return redirect('/escenarios/listar')

@login_required
def wizard_deportista_nuevo(request):
    """
    Junio 7 / 2015
    Autor: Daniel Correa

    Crear un Deportista

    A partir de POST se obtiene la información basica del deportista y se almacena en la base de datos, en caso se no haber POST se muestra el formulario vacio

    :param request: Petición Realizada
    :type request:    WSGIRequest
    """

    deportista_form = DeportistaForm()

    if request.method == 'POST':

        deportista_form = DeportistaForm(request.POST)

        if deportista_form.is_valid():
            deportista = deportista_form.save(commit=False)
            deportista.entidad =  request.tenant
            deportista.save()
            return redirect('wizard_corporal', deportista.id)


    return render(request, 'deportistas/wizard/wizard_deportista.html', {
        'titulo': 'Identificación del Deportista',
        'wizard_stage': 1,
        'form': deportista_form,
    })

@login_required
def wizard_deportista(request,id_depor):
    """
    Junio 7 / 2015
    Autor: Daniel Correa

    Editar un Deportista: Primer paso, información de identifiación del deportista

    Se obtiene el id del deportista, se busca y se almacenan los cambios

    :param request: Petición Realizada
    :type request: WSGIRequest
    :param id_depor: Llave primaria del deportista
    :type id_depor: String
    """

    try:
        deportista = Deportista.objects.get(id=id_depor)
    except Exception:
        deportista = None

    deportista_form = DeportistaForm( instance=deportista)

    if request.method == 'POST':

        deportista_form = DeportistaForm(request.POST, instance=deportista)

        if deportista_form.is_valid():
            deportista_form.save()
            return redirect('wizard_corporal', id_depor)


    return render(request, 'deportistas/wizard/wizard_deportista.html', {
        'titulo': 'Identificación del Deportista',
        'wizard_stage': 1,
        'form': deportista_form,
    })

@login_required
def wizard_corporal(request,id_depor):
    """

    Junio 7 / 2015
    Autor: Daniel Correa

    Paso para datos de composicion corporal del deportista

    Se obtiene la información de la peticion, se intenta buscar un objeto ComposicionCorporal y en caso de haber modificaciones se guardan.
    Si la informacion para la ComposicionCorporal del deportista es nueva se inicializa en nulo

    :param request: Petición Realizada
    :type request: WSGIRequest
    :param id_depor: Llave primaria del deportista
    :type id_depor: String
    """

    try:
        corporal = ComposicionCorporal.objects.get(deportista=id_depor)
    except Exception:
        corporal = None

    corporal_form = ComposicionCorporalForm(instance=corporal)

    if request.method == 'POST':
        corporal_form = ComposicionCorporalForm(request.POST, instance=corporal)

        if corporal_form.is_valid():
            corporal = corporal_form.save(commit=False)
            corporal.deportista = Deportista.objects.get(id=id_depor)
            corporal.save()
            corporal_form.save()
            return redirect('wizard_historia_deportiva', id_depor)


    return render(request, 'deportistas/wizard/wizard_corporal.html', {
        'titulo': 'Composición Corporal del Deportista',
        'wizard_stage': 2,
        'form': corporal_form,
    })

@login_required
def wizard_historia_deportiva(request,id_depor):
    pass

@login_required
def wizard_historia_academica(request,id_depor):
    pass