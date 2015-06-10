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
def registro(request):
    form = EntidadForm()

    if request.method == 'POST':
        form = EntidadForm(request.POST)
        
        if form.is_valid():
            obj = form.save(commit=False)
            obj.domain_url += settings.SUBDOMINIO_URL
            obj.save()

            messages.success(request, "Entidad registrada correctamente.")
            return redirect('entidad_registro')

    return render(request, 'entidad_registro.html', {
        'form': form,
    })