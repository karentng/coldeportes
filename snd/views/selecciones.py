from django.contrib.contenttypes.models import ContentType
from django.db import connection
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from snd.formularios.selecciones import *
from django.contrib import messages
from snd.models import *

@login_required
def registrar_base(request):
    """
    Agosto 29 / 2015
    Autor: Daniel Correa

    Permite guardar la primera seccion de la seleccion dando paso a la seleccion de deportistas y personal de apoyo

    :param request: Petición Realizada
    :type request: WSGIRequest
    """

    form = SeleccionForm()

    if request.method == 'POST':
        form = SeleccionForm(request.POST)
        if form.is_valid():
            sele = form.save()
            return redirect('registrar_deportistas',sele.id)

    return render(request,'selecciones/wizard/wizard_seleccion.html',{
        'titulo': 'Selección',
        'form': form,
        'wizard_stage': 1
    })

@login_required
def registrar_deportistas(request,id_s):
    return redirect('registrar_personal')

@login_required
def registrar_personal(request,id_s):
    return redirect('inicio_tenant')

@login_required
def listar_seleccion(request):
    """
    Agosto 30 / 2015
    Autor: Daniel Correa

    Permite listar todas las selecciones con la estrategia de cargue masivo

    :param request: Petición Realizada
    :type request: WSGIRequest
    """

    selecciones = Seleccion.objects.all()

    return render(request,'selecciones/listar_selecciones.html',{
        'selecciones': selecciones
    })