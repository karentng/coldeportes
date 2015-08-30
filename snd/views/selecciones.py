from django.contrib.contenttypes.models import ContentType
from django.db import connection
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from snd.formularios.selecciones import *

def registrar_base(request):

    form = SeleccionForm()

    return render(request,'selecciones/wizard/wizard_seleccion.html',{
        'titulo' : 'Seleccion',
        'form' : form
    })
