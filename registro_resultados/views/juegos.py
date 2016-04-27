from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.template import RequestContext
from django.http import JsonResponse, HttpResponse
from registro_resultados.models import *
from registro_resultados.forms import *
from entidades.models import *


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
def eliminar_juego(request, juego_id):

    juego= Juego.objects.get(id=juego_id)
    juego.delete()
    messages.warning(request, "Juego eliminado correctamente.")
    return redirect('listar_juegos')


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
    elif competencia.tipo_registro == 3:
        return redirect('participante_metros', competencia_id)
    
@login_required
def eliminar_participante(request, competencia_id, participante_id):

    competencia = Competencia.objects.get(id=competencia_id)
    participante = Participante.objects.get(id=participante_id, competencia=competencia_id)
    participante.delete()    
    return redirect('listar_participantes', competencia_id)        
    


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
        'individual': True,
        'puntos': True,        
        'competencia_id': competencia_id,
        'juego_id': competencia.juego.id
        
    })


@login_required
def participante_tiempos(request, competencia_id, participante_id=None):

    competencia = Competencia.objects.get(id=competencia_id)

    try:
        participante = Participante.objects.get(id=participante_id)
    except Exception:
        participante = None

    form = ParticipanteTiempoForm(competencia=competencia_id, instance=participante)

    if request.method == "POST":

        form = ParticipanteTiempoForm(request.POST, competencia=competencia_id, instance=participante)
        if form.is_valid():
            participante_nuevo = form.save(commit=False)
            participante_nuevo.competencia = competencia
            participante_nuevo.save()
            messages.success(request, "Participante registrado correctamente.")
            return redirect('listar_individual', competencia_id)
            
    return render(request, 'wizard_info_juego/wizard_crear_participante.html', {
        "form": form,
        'wizard_stage': 1,
        'individual': True,  
        'competencia_id': competencia_id,
        'juego_id': competencia.juego.id
        
    })


@login_required
def participante_metros(request, competencia_id, participante_id=None):

    competencia = Competencia.objects.get(id=competencia_id)

    try:
        participante = Participante.objects.get(id=participante_id)
    except Exception:
        participante = None

    form = ParticipanteMetrosForm(competencia=competencia, instance=participante)

    if request.method == "POST":

        form = ParticipanteMetrosForm(request.POST, competencia=competencia, instance=participante)
        if form.is_valid():
            participante_nuevo = form.save(commit=False)
            participante_nuevo.competencia = competencia
            participante_nuevo.save()
            messages.success(request, "Participante registrado correctamente.")
            return redirect('listar_individual', competencia_id)
            
    return render(request, 'wizard_info_juego/wizard_crear_participante.html', {
        "form": form,
        'wizard_stage': 1,
        'individual': True,
        'metros': True,        
        'competencia_id': competencia_id,
        'juego_id': competencia.juego.id
        
    })


@login_required
def medalleria_por_competencia(request, competencia_id):

    competencia = Competencia.objects.get(id=competencia_id)

    if competencia.tipos_participantes == 1:
        resultados1 = Participante.objects.filter(competencia=competencia_id, posicion=1)
        resultados2 = Participante.objects.filter(competencia=competencia_id, posicion=2)
        resultados3 = Participante.objects.filter(competencia=competencia_id, posicion=3)
    elif competencia.tipos_participantes == 2:
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

    competencia = Competencia.objects.get(id=competencia_id)    
    equipo = Equipo.objects.get(id=participante_id, competencia=competencia_id)
    equipo.delete()

    return redirect('listar_equipos', competencia_id)
    

@login_required
def datos_equipo(request, competencia_id):

    competencia = Competencia.objects.get(id=competencia_id)
    
    if competencia.tipo_registro == 1:
        return redirect('equipo_tiempos', competencia_id)
    elif competencia.tipo_registro == 2:
        return redirect('equipo_puntos', competencia_id)
    elif competencia.tipo_registro == 3:
        return redirect('equipo_metros', competencia_id)
        

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
    puntos = False
    metros = None

    if competencia.tipo_registro == 1:
        puntos = False
    elif competencia.tipo_registro == 2:
        puntos = True
    elif competencia.tipo_registro == 3:
        metros = True
    return render(request, 'wizard_info_juego/wizard_participantes.html', {
        'wizard_stage': 1,
        'participantes': participantes,
        'competencia_id': competencia_id,
        'juego_id': competencia.juego.id,
        'individual': True,
        'puntos': puntos,
        'metros': metros
    })


@login_required
def listar_equipos(request, competencia_id):

    equipos = Equipo.objects.filter(competencia=competencia_id) or None
    competencia = Competencia.objects.get(id=competencia_id)
    puntos = False
    metros = None

    if competencia.tipo_registro == 1:
        puntos = False
    elif competencia.tipo_registro == 2:
        puntos = True
    elif competencia.tipo_registro == 3:
        metros = True

    return render(request, 'wizard_info_juego/wizard_participantes.html', {
        'wizard_stage': 1,
        'participantes': equipos,
        'competencia_id': competencia_id,
        'juego_id': competencia.juego.id,
        'puntos': puntos,
        'metros': metros
    })


@login_required
def equipo_puntos(request, competencia_id, equipo_id=None):

    competencia = Competencia.objects.get(id=competencia_id)
    
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
    

@login_required
def equipo_tiempos(request, competencia_id, equipo_id=None):

    competencia = Competencia.objects.get(id=competencia_id)
    
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

    
@login_required
def equipo_metros(request, competencia_id, equipo_id=None):

    competencia = Competencia.objects.get(id=competencia_id)
    
    try:
        equipo = Equipo.objects.get(id=equipo_id)
    except Exception:
        equipo = None

    form = EquipoMetrosForm(instance=equipo)

    if request.method == "POST":
        form = EquipoMetrosForm(request.POST, instance=equipo)

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
        'juego_id': competencia.juego.id,
        'metros': True


    })


#Ajax para modalidad y categoria historia deportiva
@login_required
def get_modalidades(request,deporte_id):

    modalidades = ModalidadDisciplinaDeportiva.objects.filter(deporte=deporte_id)
    if modalidades:
        print('lekrokerl')
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


# cargar por excel
@login_required
def cargas_competencias(request, juego_id):

    try:
        juego = Juego.objects.get(id=juego_id)
    except Exception:
        return redirect("listar_juegos")

    form = CompetenciasBaseDeDatos()

    if request.method == 'POST':
        form = CompetenciasBaseDeDatos(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['archivo']
            nombre = archivo.name.split('.')

            FORMATOS_PERMITIDOS = ['csv', 'xls', 'xlsx']

            if nombre[len(nombre)-1] in FORMATOS_PERMITIDOS:
                try:
                    competencias, datemode = leer_competencias(request, archivo)
                except:
                    messages.error(request, 'La primera hoja del archivo debe llamarse: Hoja1')
                    return redirect('cargas_competencias', juego_id) 
                try:
                    crear_competencias(request, competencias, datemode, juego) 
                    messages.success(request, "Competencias Cargadas Satisfactoriamente")
                    return redirect('listado_competencias', juego_id)
                except:
                    messages.error(request, "El archivo no se encuentra en el formato correcto.")
                    return redirect('cargas_competencias', juego_id) 
            else:
                from django.forms.util import ErrorList
                errors = form._errors.setdefault("archivo", ErrorList())
                errors.append(u"Error de formato, debe ser CSV, XLS o XLSX")

    return render(request, 'cargado_archivos/cargas_competencias.html', {
        'form': form,
        'juego_id': juego_id,
    })


@login_required
def crear_competencias(request, competencias, datemode, juego):

    import xlrd
    import datetime
    for competencia in competencias:
        obj = Competencia()
        obj.nombre = competencia[0]

        date = datetime.datetime(1899, 12, 30)
        get_col2 = str(date + datetime.timedelta(competencia[1]))[:10]
        d = datetime.datetime.strptime(get_col2, "%Y-%m-%d")

        obj.fecha_competencia = d.strftime("%Y-%m-%d")#xlrd.xldate_as_tuple(competencia[1], datemode)
        obj.tipo_competencia = competencia[2]
        obj.tipo_registro = competencia[3]
        obj.lugar = competencia[4]
        obj.tipos_participantes = competencia[5]
        obj.deporte = TipoDisciplinaDeportiva.objects.get(id=competencia[6])
        obj.descripcion =  competencia[9]

        try:
            categoria = CategoriaDisciplinaDeportiva.objects.get(id=competencia[7]) or None
            obj.categoria = categoria

        except:
            obj.categoria = None
            
        try:
            modalidad = ModalidadDisciplinaDeportiva.objects.get(id=competencia[8]) or None
            obj.modalidad = modalidad
        except:
            obj.modalidad = None            

        obj.juego = juego
        obj.save()


@login_required
def leer_competencias(request, archivo):
    
    import xlrd
    archivo = archivo.read()
    excel = xlrd.open_workbook(file_contents=archivo)

    hoja = excel.sheet_by_name('Hoja1')

    numero_filas = hoja.nrows 
    numero_celdas = hoja.ncols
    fila_actual = 1 # -1 para tomar la primera linea
    competencias = []
    while fila_actual < numero_filas:
        datos = []
        celda_actual = 0

        while celda_actual < numero_celdas:
            valor = hoja.cell(fila_actual, celda_actual).value
            datos.append(valor)
            celda_actual += 1

        competencias.append(datos)
        fila_actual += 1
    return [competencias, excel.datemode]


@login_required
def cargar_participantes(request, competencia_id):
    try:
        competencia = Competencia.objects.get(id=competencia_id)
    except Exception:
        return redirect("listar_juegos")

    form = ParticipantesBaseDeDatos()

    if request.method == 'POST':
        form = ParticipantesBaseDeDatos(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['archivo']
            nombre = archivo.name.split('.')

            FORMATOS_PERMITIDOS = ['csv', 'xls', 'xlsx']

            if nombre[len(nombre)-1] in FORMATOS_PERMITIDOS:
                try:
                    participantes, datemode = leer_competencias(request, archivo)
                except:
                    messages.error(request, 'La primera hoja del archivo debe llamarse: Hoja1')
                    return redirect('cargar_participantes', competencia_id)
                try:
                    crear_participantes(request, participantes, datemode, competencia)
                    messages.success(request, "Participantes subidos correctamente.")
                    return redirect('listar_participantes', competencia_id)                    
                except:
                    messages.error(request, "El archivo no se encuentra en el formato correcto.")
                    return redirect('cargar_participantes', competencia_id)
            else:
                from django.forms.util import ErrorList
                errors = form._errors.setdefault("archivo", ErrorList())
                errors.append(u"Error de formato, debe ser CSV, XLS o XLSX")

    return render(request, 'cargado_archivos/cargar_participantes.html', {
        'form': form,
        'competencia_id': competencia.id,
        'wizard_stage': 3,
    })


@login_required
def crear_participantes(request, participantes, datemode, competencia):
    import xlrd
    import datetime
    for participante in participantes:
        obj = Participante()

        obj.nombre = participante[0]
        obj.genero = participante[1]
        obj.departamento = Departamento.objects.get(id=participante[2])
        obj.club = participante[3] or None

        date = datetime.datetime(1899, 12, 30)
        get_col2 = str(date + datetime.timedelta(participante[4]))[:10]
        d = datetime.datetime.strptime(get_col2, "%Y-%m-%d")
        obj.fecha_nacimiento = d.strftime("%Y-%m-%d")
        obj.estatura = participante[5] or None
        obj.peso = participante[6] or None
        obj.posicion = participante[7]
        obj.competencia = competencia
        if competencia.tipos_participantes == 1: #Individual
            if competencia.tipo_registro == 1: # Tiempos
                obj.tiempo = participante[10]
                obj.marca = participante[11]
            elif competencia.tipo_registro == 2: # Puntos
                obj.puntos = participante[9]                
            else: # Metros
                obj.metros = participante[8]
                obj.marca = participante[11]                
        else: # Equipos
            obj.equipo = Equipo.objects.get(id=participante[12])
        try: 
            obj.save()
        except Exception as e:
            print(e)
