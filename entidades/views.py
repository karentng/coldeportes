import os
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from entidades.models import *
from entidades.forms import *
from django.conf import settings
from django.contrib import messages

@login_required
def tipo(request):
    return render(request, 'entidad_tipo.html', {
    })

@login_required
def registro(request, tipo):
    form = EntidadForm()
    form2 = ActoresForm()

    dominio = settings.SUBDOMINIO_URL

    if request.method == 'POST':
        form = EntidadForm(request.POST)
        form2 = ActoresForm(request.POST)
        if form.is_valid() and form2.is_valid():
            actores = form2.save()

            pagina = form.cleaned_data['pagina']
            obj = form.save(commit=False)
            obj.schema_name = pagina
            obj.domain_url = pagina + dominio
            obj.actores = actores
            obj.tipo = tipo
            obj.save()

            messages.success(request, "Entidad registrada correctamente.")
            return redirect('entidad_registro', tipo)

    return render(request, 'entidad_registro.html', {
        'form': form,
        'form2': form2,
        'dominio': dominio,
    })

def listar_entrenadores_nacionales(request):
    pass

def listar_dirigentes_nacionales(request):
    pass

def listar_deportistas_nacionales(request):
    pass

def listar_escenarios_nacionales(request):
    pass

def listar_cajas_nacionales(request):
    pass

def listar_cafs_nacionales(request):
    pass