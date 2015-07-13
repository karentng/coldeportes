import os
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from entidades.models import *
from entidades.forms import *
from django.conf import settings
from django.contrib import messages
from snd.modelos.cafs import CentroAcondicionamiento

@login_required
def tipo(request):
    return render(request, 'entidad_tipo.html', {
    })

@login_required
def registro(request):
    form = EntidadForm()
    dominio = settings.SUBDOMINIO_URL

    if request.method == 'POST':
        form = EntidadForm(request.POST)
        
        if form.is_valid():
            pagina = form.cleaned_data['pagina']
            obj = form.save(commit=False)
            obj.schema_name = pagina
            obj.domain_url = pagina + dominio
            obj.save()

            messages.success(request, "Entidad registrada correctamente.")
            return redirect('entidad_registro')

    return render(request, 'entidad_registro.html', {
        'form': form,
        'dominio': dominio,
    })