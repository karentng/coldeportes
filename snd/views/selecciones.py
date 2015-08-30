from django.contrib.contenttypes.models import ContentType
from django.db import connection
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from snd.formularios.selecciones import *
from django.contrib import messages

@login_required
def registrar_base(request):

    form = SeleccionForm()

    if request.method == 'POST':
        form = SeleccionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registrar_deportistas')

    return render(request,'selecciones/wizard/wizard_seleccion.html',{
        'titulo': 'Selección',
        'form': form,
        'wizard_stage': 1
    })

@login_required
def registrar_deportistas(request,id_s):
    return redirect('inicio_tenant')

@login_required
def registrar_personal(request,id_s):
    pass