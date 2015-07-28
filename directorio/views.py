from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from directorio.forms import *

# Create your views here.
@login_required
def directorio_buscar(request):
    """
    Julio 22 / 2015
    Autor: Karent Narvaez Grisales
    
    realizar búsqueda de los diferentes criterios para un contacto en el directorio.

    Se obtienen los escenario que ha registrado el tenant que realiza la petición

    :param request:   Petición realizada
    :type request:    WSGIRequest
    """

    form = DirectorioBusquedaForm()
    return render(request, 'directorio_buscar.html', {
    	'form': form,
    })