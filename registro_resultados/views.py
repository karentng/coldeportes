from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.template import RequestContext
from entidades.models import *
from django.http import JsonResponse,HttpResponse
from registro_resultados.models import *
from registro_resultados.forms import *


@login_required
def registrar_juego(request, juego_id=None):
    try:
        juego = Juego.objects.get(id=juego_id)
    except Exception:
        juego = None

    form = JuegoForm(instance=juego)

    if request.method == "POST":
        
        form = JuegoForm(request.POST, request.FILES, instance=juego)

        if form.is_valid():
            form.save()
            messages.success(request, "Juego registrado correctamente.")
            return redirect('listar_juegos')
    return render(request, 'registro_juego.html', {
        "form": form,
    })

@login_required
def listar_juegos(request):
    juegos = Juego.objects.all()
    return render(request, 'listado_juegos.html', {
        "juegos": juegos,
    })

@login_required
def datos_competencia(request, juego_id, competencia_id=None):
    try:
        juego = Juego.objects.get(id=juego_id)
        competencia = Competencia.objects.get(id=competencia_id)
    except Exception:
        competencia = None

    form = CompetenciaForm(instance=competencia)

    if request.method == "POST":
        deporte_id = request.POST['deporte']
        form = CompetenciaForm(request.POST, request.FILES, deporte_id=deporte_id, instance=competencia)

        if form.is_valid():
            nueva_competencia = form.save(commit=False)
            nueva_competencia.juego = juego
            nueva_competencia.save()
            messages.success(request, "Competencia registrada correctamente.")
            return redirect('listado_competencias', juego_id)
    return render(request, 'registro_competencia.html', {
        "form": form,
        'juego_id': juego_id,
    })


@login_required
def listado_competencias(request, juego_id):
    competencias = Competencia.objects.filter(juego=juego_id)

    return render(request, 'listado_competencias.html', {
        'juego_id': juego_id,
        'competencias': competencias,
    })

@login_required
def eliminar_competencia(request, juego_id, competencia_id):
    competencia = Competencia.objects.get(id=competencia_id, juego=juego_id)
    competencia.delete()
    messages.warning(request, "Competencia eliminada correctamente.")
    return redirect('listado_competencias', juego_id)


@login_required
def crear_participante(request, competencia_id):
    competencia = Competencia.objects.get(id=competencia_id)
    
    if competencia.tipos_participantes == 1:
        return redirect('datos_participante', competencia_id)
    else:
        return redirect('datos_equipo', competencia_id)


@login_required
def datos_participante(request, competencia_id):
    competencia = Competencia.objects.get(id=competencia_id)

    if competencia.tipo_registro == 1:
        return redirect('participante_tiempos', competencia_id)
    elif competencia.tipo_registro == 2:
        return redirect('participante_puntos', competencia_id)
    
@login_required
def eliminar_participante(request, competencia_id, participante_id):
    participante = Participante.objects.get(id=participante_id, competencia=competencia_id)
    participante.delete()

    if request.session['puntos']==0:
        return redirect('participante_puntos', competencia_id)
    elif request.session['puntos']==1:
        return redirect('participante_tiempos', competencia_id)
    else:
        return redirect('participante_equipo', competencia_id)


@login_required
def participante_equipo(request, competencia_id, equipo_id, participante_id=None):
    competencia = Competencia.objects.get(id=competencia_id)
    equipo = Equipo.objects.get(id=equipo_id)
    participantes = Participante.objects.filter(competencia=competencia_id, equipo=equipo_id)

    try:
        participante = Participante.objects.get(id=participante_id)
    except Exception:
        participante = None


    form = ParticipanteEquipoForm(competencia=competencia, instance=participante)

    if request.method == "POST":

        form = ParticipanteEquipoForm(request.POST, competencia=competencia, instance=participante)
        if form.is_valid():
            participante_nuevo = form.save(commit=False)
            participante_nuevo.competencia = competencia
            participante_nuevo.equipo = equipo
            participante_nuevo.save()
            messages.success(request, "Participante registrado correctamente.")
            return redirect('participante_equipo', competencia_id, equipo_id)
            
    return render(request, 'wizard_info_juego/wizard_participantes_equipo.html', {
        "form": form,
        'wizard_stage': 1,
        'participantes': participantes,
        'competencia_id': competencia_id,
        'juego_id': competencia.juego.id,
        'equipo': equipo
        
    })

@login_required
def participante_puntos(request, competencia_id, participante_id=None):
    competencia = Competencia.objects.get(id=competencia_id)
    participantes = Participante.objects.filter(competencia=competencia_id)
    request.session['puntos']=0

    try:
        participante = Participante.objects.get(id=participante_id)
    except Exception:
        participante = None


    form = ParticipantePuntosForm(competencia=competencia, instance=participante)

    if request.method == "POST":

        form = ParticipantePuntosForm(request.POST, competencia=competencia, instance=participante)
        if form.is_valid():
            participante_nuevo = form.save(commit=False)
            participante_nuevo.competencia = competencia
            participante_nuevo.save()
            messages.success(request, "Participante registrado correctamente.")
            return redirect('listar_individual', competencia_id)
            
    return render(request, 'wizard_info_juego/wizard_crear_participante.html', {
        "form": form,
        'wizard_stage': 1,
        'participantes': participantes,
        'individual': True,
        'puntos': True,        
        'competencia_id': competencia_id,
        'juego_id': competencia.juego.id
        
    })

@login_required
def participante_tiempos(request, competencia_id, participante_id=None):
    competencia = Competencia.objects.get(id=competencia_id)
    request.session['puntos']=1

    try:
        participante = Participante.objects.get(id=participante_id)
    except Exception:
        participante = None


    form = ParticipanteTiempoForm(competencia=competencia, instance=participante)

    if request.method == "POST":

        form = ParticipanteTiempoForm(request.POST, competencia=competencia, instance=participante)
        if form.is_valid():
            participante_nuevo = form.save(commit=False)
            participante_nuevo.competencia = competencia
            participante_nuevo.save()
            messages.success(request, "Participante registrado correctamente.")
            return redirect('listar_individual', competencia_id)
            
    return render(request, 'wizard_info_juego/wizard_participantes.html', {
        "form": form,
        'wizard_stage': 1,
        'individual': True,  
        'competencia_id': competencia_id,
        'juego_id': competencia.juego.id
        
    })


@login_required
def medalleria_por_competencia(request, competencia_id):
    competencia = Competencia.objects.get(id=competencia_id)

    if request.session['puntos']==0:
        resultados1 = Participante.objects.filter(competencia=competencia_id, posicion=1)
        resultados2 = Participante.objects.filter(competencia=competencia_id, posicion=2)
        resultados3 = Participante.objects.filter(competencia=competencia_id, posicion=3)
    elif request.session['puntos']==1:
        resultados1 = Equipo.objects.filter(competencia=competencia_id, posicion=1)
        resultados2 = Equipo.objects.filter(competencia=competencia_id, posicion=2)
        resultados3 = Equipo.objects.filter(competencia=competencia_id, posicion=3)

    return render(request, 'wizard_info_juego/wizard_medalleria.html', {
        'wizard_stage': 2,
        'competencia_id': competencia_id,
        'juego_id': competencia.juego.id,
        'individual': True,
        'resultados1': resultados1,
        'resultados2':resultados2,
        'resultados3': resultados3


    })

@login_required
def eliminar_equipo(request, competencia_id, participante_id):
    equipo = Equipo.objects.get(id=participante_id, competencia=competencia_id)
    equipo.delete()

    if request.session['puntos']==0:
        return redirect('equipo_puntos', competencia_id)
    elif request.session['puntos']==1:
        return redirect('equipo_tiempos', competencia_id)

@login_required
def datos_equipo(request, competencia_id):
    competencia = Competencia.objects.get(id=competencia_id)
    
    if competencia.tipo_registro == 1:
        return redirect('equipo_tiempos', competencia_id)
    elif competencia.tipo_registro == 2:
        return redirect('equipo_puntos', competencia_id)
        

@login_required
def listar_participantes(request, competencia_id):
    competencia = Competencia.objects.get(id=competencia_id)

    if competencia.tipos_participantes == 1:
        return redirect('listar_individual', competencia_id)
    else:
        return redirect('listar_equipos', competencia_id)

@login_required
def listar_individual(request, competencia_id):
    participantes = Participante.objects.filter(competencia=competencia_id) or None
    competencia = Competencia.objects.get(id=competencia_id)

    if competencia.tipo_registro == 1:
        puntos = False
    elif competencia.tipo_registro == 2:
        puntos = True

    return render(request, 'wizard_info_juego/wizard_participantes.html', {
        'wizard_stage': 1,
        'participantes': participantes,
        'competencia_id': competencia_id,
        'juego_id': competencia.juego.id,
        'individual': True,
        'puntos': puntos


    })

@login_required
def listar_equipos(request, competencia_id):
    equipos = Equipo.objects.filter(competencia=competencia_id) or None
    competencia = Competencia.objects.get(id=competencia_id)

    if competencia.tipo_registro == 1:
        puntos = False
    elif competencia.tipo_registro == 2:
        puntos = True

    return render(request, 'wizard_info_juego/wizard_participantes.html', {
        'wizard_stage': 1,
        'participantes': equipos,
        'competencia_id': competencia_id,
        'juego_id': competencia.juego.id,
        'puntos': puntos


    })


@login_required
def equipo_puntos(request, competencia_id, equipo_id=None):
    competencia = Competencia.objects.get(id=competencia_id)
    request.session['puntos']=0
    
    try:
        equipo = Equipo.objects.get(id=equipo_id)
    except Exception:
        equipo = None


    form = EquipoPuntosForm(instance=equipo)

    if request.method == "POST":
        form = EquipoPuntosForm(request.POST, instance=equipo)

        if form.is_valid():
            equipo_nuevo = form.save(commit=False)
            equipo_nuevo.competencia = competencia
            equipo_nuevo.save()
            messages.success(request, "Equipo registrado correctamente.")

            return redirect('listar_equipos', competencia_id)

    return render(request, 'wizard_info_juego/wizard_crear_participante.html', {
        'form': form,
        'wizard_stage': 1,
        'puntos': True,
        'competencia_id': competencia_id,
        'juego_id': competencia.juego.id


    })
    
@login_required
def equipo_tiempos(request, competencia_id, equipo_id=None):
    competencia = Competencia.objects.get(id=competencia_id)
    request.session['puntos']=1
    
    try:
        equipo = Equipo.objects.get(id=equipo_id)
    except Exception:
        equipo = None


    form = EquipoTiempoForm(instance=equipo)

    if request.method == "POST":
        form = EquipoTiempoForm(request.POST, instance=equipo)

        if form.is_valid():
            equipo_nuevo = form.save(commit=False)
            equipo_nuevo.competencia = competencia
            equipo_nuevo.save()
            messages.success(request, "Equipo registrado correctamente.")

            return redirect('listar_equipos', competencia_id)

    return render(request, 'wizard_info_juego/wizard_crear_participante.html', {
        'form': form,
        'wizard_stage': 1,
        'competencia_id': competencia_id,
        'juego_id': competencia.juego.id


    })



#Ajax para modalidad y categoria historia deportiva
@login_required
def get_modalidades(request,deporte_id):
    modalidades = ModalidadDisciplinaDeportiva.objects.filter(deporte=deporte_id)
    if modalidades:
        data = []
        for m in modalidades:
            dic = {}
            dic['id'] = m.id
            dic['text'] = m.nombre
            data.append(dic)
    else:
        return HttpResponse('Modalidades no encontradas',status=404)
    return JsonResponse({
        'data': data
    })

@login_required
def get_categorias(request,deporte_id):
    categorias = CategoriaDisciplinaDeportiva.objects.filter(deporte=deporte_id)
    if categorias:
        data = []
        for c in categorias:
            dic = {}
            dic['id'] = c.id
            dic['text'] = c.nombre
            data.append(dic)
    else:
        return HttpResponse('Categorias no encontradas',status=404)
    return JsonResponse({
        'data': data
    })