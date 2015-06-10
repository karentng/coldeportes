from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
#from django.core.files.storage import FileSystemStorage
#import os
from snd.formularios.dirigentes  import *

@login_required
def crearDirigente(request):
	if request == 'POST':
		return HttpResponse("Hola Dirigentes Nuevo")
	else:
		form = CrearDirigenteForm();
		return render(request, 'dirigentes/nuevo.html', {'form':form})

@login_required
def listarDirigentes(request):
    return HttpResponse("Hola Dirigentes Lista")