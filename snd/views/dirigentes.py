from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
#from django.core.files.storage import FileSystemStorage
#import os
from snd.formularios.dirigentes  import *

@login_required
def crearDirigente(request):
	if request.method == 'POST':
		form = CrearDirigenteForm(request.POST)
		if form.is_valid():
			dirigente = form.save(commit=False)
			dirigente.entidad = request.tenant
			form.save()
			messages.success(request, "Dirigente registrado correctamente.")
			return redirect('dirigentes_crear')
	else:
		form = CrearDirigenteForm();
		return render(request, 'dirigentes/nuevo.html', 
			{'titulo':'Datos del dirigente',
			'form':form})

@login_required
def listarDirigentes(request):
    return HttpResponse("Hola Dirigentes Lista")