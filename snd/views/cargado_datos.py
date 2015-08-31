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
# Filtrado de datos para listar
#==================================================================

@login_required
def cargar_datos(request, modelo):
    from snd.cargado_datos import obtenerDatos
    from django.http import JsonResponse

    datos = obtenerDatos(request, int(modelo))

    return JsonResponse(datos)

@login_required
def cargar_columnas(request, modelo):
    from snd.cargado_datos import obtenerCantidadColumnas
    from django.http import JsonResponse

    datos = obtenerCantidadColumnas(request, int(modelo))

    return JsonResponse(datos)