from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.template import RequestContext

from registro_resultados.models import *
from registro_resultados.forms import *

@login_required
def obtener_competencia_session(request):
    try:
        idCompetencia = request.session['competencia_seleccionada_id']
        competencia = Competencia.objects.get(id=idCompetencia)
        return competencia
    except Exception:
        return None

@login_required
def datos_competencia(request, idCompetencia=None):
    try:
        competencia = Competencia.objects.get(id=idCompetencia)
    except Exception:
        competencia = None

    form = CompetenciaForm(instance=competencia)
    if request.method == "POST":
        form = CompetenciaForm(request.POST, request.FILES, instance=competencia)
        if form.is_valid():
            form.save()
            messages.success(request, "Competencia registrada correctamente.")
            return redirect('listado_competencias')
    return render(request, 'registro_competencia.html', {
        "form": form,
    })

@login_required
def listado_competencias(request):
    competencias = Competencia.objects.all()
    return render(request, 'listado_competencias.html', {
        "competencias": competencias,
    })

@login_required
def acceder_competencia(request, idCompetencia):
    try:
        Competencia.objects.get(id=idCompetencia)
        request.session['competencia_seleccionada_id'] = idCompetencia
        messages.success(request, "Competencia seleccionada correctamente.")
        return redirect('menu_competencia')
    except Exception:
        messages.success(request, "La Competencia indicada no existe por favor seleccione una del listado.")
        return redirect('listado_competencias')

@login_required
def menu_competencia(request):
    competencia = obtener_competencia_session(request)
    if not competencia:
        return redirect('listado_competencias')

    if competencia.tipos_participantes == 1: # Individual
        titulos = ["Nombres", "Apellidos", "Género", "Categoría", "Departamento", "Posición", "Tiempo"]
        datos = Participante.objects.filter(competencia=competencia)
    else:
        titulos = ["Nombres", "Departamento", "Posición"]
        datos = Equipo.objects.filter(competencia=competencia)

    return render(request, 'menu_competencia.html', {
        "competencia": competencia,
        "titulos": titulos,
        "datos": datos,
    })

@login_required
def datos_participante(request, idParticipante=None):
    competencia = obtener_competencia_session(request)
    if not competencia:
        return redirect('listado_competencias')

    try:
        participante = Participante.objects.get(id=idParticipante)
    except Exception:
        participante = None

    form = ParticipanteForm(competencia=competencia, instance=participante)
    if request.method == "POST":
        form = ParticipanteForm(request.POST, competencia=competencia, instance=participante)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.competencia = competencia
            obj.save()
            messages.success(request, "Participante registrado correctamente.")
            return redirect('menu_competencia')
    return render(request, 'registrar_participante.html', {
        "form": form,
    })

@login_required
def datos_equipo(request, idEquipo=None):
    competencia = obtener_competencia_session(request)
    if not competencia:
        return redirect('listado_competencias')

    try:
        equipo = Equipo.objects.get(id=idEquipo)
    except Exception:
        equipo = None

    form = EquipoForm(instance=equipo)
    if request.method == "POST":
        form = EquipoForm(request.POST, instance=equipo)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.competencia = competencia
            obj.save()
            messages.success(request, "Equipo registrado correctamente.")
            return redirect('menu_competencia')
    return render(request, 'registrar_equipo.html', {
        "form": form,
    })

@login_required
def crear_participante(request):
    competencia = obtener_competencia_session(request)
    if not competencia:
        return redirect('listado_competencias')

    if competencia.tipos_participantes == 1:
        return redirect('datos_participante')
    else:
        return redirect('datos_equipo')