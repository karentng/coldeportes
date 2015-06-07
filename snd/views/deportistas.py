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

def crear_deportista(request):
    return redirect('/escenarios/listar')

def desactivar_deportista(request):
    return redirect('/escenarios/listar')

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
    pass

@login_required
def wizard_corporal(request,id_depor):
    pass
