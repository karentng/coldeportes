import os
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from entidades.models import *
from entidades.forms import *
from django.conf import settings
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.db import connection
from snd.modelos.entrenadores import *
from snd.modelos.escenarios import *
from snd.modelos.deportistas import *
from snd.modelos.cafs import *
from snd.modelos.cajas_compensacion import *
from snd.modelos.dirigentes import *
from coldeportes.utilities import calculate_age


@login_required
def tipo(request):
    return render(request, 'entidad_tipo.html', {
        'tenant_nacional':True
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
        'tenant_nacional':True
    })

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
@csrf_exempt
def test(request):
    from django.contrib.auth.models import User
    from django.contrib.auth import authenticate, login

    if request.method == 'GET':
        username = request.GET['name']
        password = request.GET['pw']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                return JsonResponse({'id': user.id})

    return JsonResponse({'id': None})

from snd.modelos.cafs import *
def cafs(request):
    entidad = Entidad.objects.get(schema_name='cliente1')
    connection.set_tenant(entidad)
    centros = CentroAcondicionamiento.objects.all()
    datos = {'escenarios':[], 'cafs':[]} # [Escenarios, CAFS]
    for i in centros:
        dato = {
            'id': i.id,
            'nombre': i.nombre,
            'latitud': i.latitud,
            'longitud': i.longitud,
            'sincronizar': False,
        }
        datos['cafs'].append(dato)
    return JsonResponse(datos)

def actualizarLocalizacionCaf(actor):
    centro = CentroAcondicionamiento.objects.get(id=actor['id'])
    centro.latitud = actor['latitud']
    centro.longitud = actor['longitud']
    centro.save()

import json
def actualizarLocalizacion(request):
    if request.method == 'GET':
        entidad = Entidad.objects.get(schema_name='cliente1')
        connection.set_tenant(entidad)

        tipoActor = request.GET['tipoActor']
        actor = json.loads(request.GET['actor'])

        if tipoActor == '1':
            actualizarLocalizacionCaf(actor)
            return JsonResponse({'response': True})

def sincronizar(request):
    if request.method == 'GET':
        entidad = Entidad.objects.get(schema_name='cliente1')
        connection.set_tenant(entidad)

        escenarios = json.loads(request.GET.get('escenarios', '[]'))
        cafs = json.loads(request.GET.get('cafs', '[]'))

        for i in cafs:
            actualizarLocalizacionCaf(i)

        return JsonResponse({'response': True})


#==================================================================
# Filtrado de datos para listar
#==================================================================

def cargar_datos_tenantnacional(request, modelo):
    from entidades.cargado_datos_tenantnacional import obtenerDatos
    from django.http import JsonResponse
    try:
        datos = obtenerDatos(request, int(modelo))
    except Exception as e:
        print(e)

    return JsonResponse(datos)

def cargar_columnas_tenantnacional(request, modelo):
    from entidades.cargado_datos_tenantnacional import obtenerCantidadColumnas
    from django.http import JsonResponse

    datos = obtenerCantidadColumnas(request, int(modelo))

    return JsonResponse(datos)


def listar_entrenadores_nacionales(request):
    return render(request,'tenant_nacional/entrenadores_listar.html',{'tenant_nacional':True})

def listar_dirigentes_nacionales(request):
    return render(request,'tenant_nacional/dirigentes_listar.html',{'tenant_nacional':True})

def listar_deportistas_nacionales(request):
    return render(request,'tenant_nacional/deportistas_listar.html',{'tenant_nacional':True})

def listar_escenarios_nacionales(request):
    return render(request,'tenant_nacional/escenarios_listar.html',{'tenant_nacional':True})

def listar_cajas_nacionales(request):
    return render(request,'tenant_nacional/cajas_listar.html',{'tenant_nacional':True})

def listar_cafs_nacionales(request):
    return render(request,'tenant_nacional/cafs_listar.html',{'tenant_nacional':True})

def ver_entrenador_tenantnacional(request, id_entrenador, tenant):
    """
    Agosto 11 /2015
    Autor: Milton Lenis

    Ver Entrenador en el tenant nacional
    Se identifica el tenant al que pertenece un entrenador y se busca
    Se obtiene la informacion general del entrenador desde la base de datos y se muestra

    :param request: Petición Realizada
    :type request: WSGIRequest
    :param id_entrenador: Llave primaria del entrenador
    :type id_entrenador: String
    :param tenant: Nombre del esquema del tenant
    :type tenant: String
    """
    try:
        entidad = Entidad.objects.get(nombre=tenant)
    except Exception:
        messages.error(request, "Error: La entidad solicitada no existe")
        return redirect('listar_entrenadores_nacionales')

    connection.set_tenant(entidad)
    ContentType.objects.clear_cache()
    try:
        entrenador = Entrenador.objects.get(id=id_entrenador)
    except:
        messages.error(request, "Error: No existe el entrenador solicitado o su información es incompleta")
        return redirect('listar_entrenadores_nacionales')
    formacion_deportiva = FormacionDeportiva.objects.filter(entrenador=entrenador)
    experiencia_laboral = ExperienciaLaboral.objects.filter(entrenador=entrenador)
    entrenador.edad = calculate_age(entrenador.fecha_nacimiento)

    return render(request,'entrenadores/ver_entrenador.html',{
            'entrenador':entrenador,
            'formacion_deportiva':formacion_deportiva,
            'experiencia_laboral':experiencia_laboral,
            'tenant_nacional':True
        })

def ver_escenario_tenantnacional(request, id_escenario, tenant):
    """
    Agosto 11 /2015
    Autor: Milton Lenis

    Ver Escenario en el tenant nacional
    Se identifica el tenant al que pertenece un escenario y se busca
    Se obtiene la informacion general del escenario desde la base de datos y se muestra

    :param request: Petición Realizada
    :type request: WSGIRequest
    :param id_escenario: Llave primaria del escenario
    :type id_escenario: String
    :param tenant: Nombre del esquema del tenant
    :type tenant: String
    """
    try:
        entidad = Entidad.objects.get(nombre=tenant)
    except Exception:
        messages.error(request, "Error: La entidad solicitada no existe")
        return redirect('listar_escenarios_nacionales')

    connection.set_tenant(entidad)
    ContentType.objects.clear_cache()
    try:
        escenario = Escenario.objects.get(id=id_escenario)
    except Exception:
        messages.error(request, "Error: El escenario no existe")
        return redirect('listar_escenarios_nacionales')
    caracteristicas = CaracterizacionEscenario.objects.filter(escenario=escenario)
    horarios = HorarioDisponibilidad.objects.filter(escenario=escenario)
    fotos = Foto.objects.filter(escenario=escenario)
    videos =  Video.objects.filter(escenario=escenario)
    historicos =  DatoHistorico.objects.filter(escenario=escenario)
    contactos = Contacto.objects.filter(escenario=escenario)

    return render(request, 'escenarios/ver_escenario.html', {
        'escenario': escenario,
        'caracteristicas': caracteristicas,
        'horarios': horarios,
        'historicos': historicos,
        'fotos': fotos,
        'videos': videos,
        'contactos': contactos,
        'tenant_nacional': True
    })

def ver_deportista_tenantnacional(request, id_depor, tenant):
    """
    Agosto 11 /2015
    Autor: Milton Lenis

    Ver Deportista en el tenant nacional
    Se identifica el tenant al que pertenece un deportista y se busca
    Se obtiene la informacion general del deportista desde la base de datos y se muestra

    :param request: Petición Realizada
    :type request: WSGIRequest
    :param id_depor: Llave primaria del deportista
    :type id_depor: String
    :param tenant: Nombre del esquema del tenant
    :type tenant: String
    """
    try:
        entidad = Entidad.objects.get(nombre=tenant)
    except Exception:
        messages.error(request, "Error: La entidad solicitada no existe")
        return redirect('listar_deportistas_nacionales')

    connection.set_tenant(entidad)
    ContentType.objects.clear_cache()
    try:
        deportista = Deportista.objects.get(id=id_depor)
    except:
        messages.error(request, "Error: No existe el deportista solicitado")
        return redirect('listar_deportistas_nacionales')
    composicion = ComposicionCorporal.objects.filter(deportista=deportista)
    if len(composicion) != 0:
        composicion = composicion[0]
    historial_deportivo = HistorialDeportivo.objects.filter(deportista=deportista)
    informacion_academica = InformacionAcademica.objects.filter(deportista=deportista)
    deportista.edad = calculate_age(deportista.fecha_nacimiento)
    deportista.disciplinas_str = ','.join(x.descripcion for x in deportista.disciplinas.all())
    return render(request,'deportistas/ver_deportista.html',{
            'deportista':deportista,
            'composicion':composicion,
            'historial_deportivo':historial_deportivo,
            'informacion_academica':informacion_academica,
            'tenant_nacional':True
        })

def ver_dirigente_tenantnacional(request, id_dirigente, tenant):
    """
    Agosto 11 /2015
    Autor: Milton Lenis

    Ver Dirigente en el tenant nacional
    Se identifica el tenant al que pertenece un dirigente y se busca
    Se obtiene la informacion general del dirigente desde la base de datos y se muestra

    :param request: Petición Realizada
    :type request: WSGIRequest
    :param id_dirigente: Llave primaria del dirigente
    :type id_dirigente: String
    :param tenant: Nombre del esquema del tenant
    :type tenant: String
    """
    try:
        entidad = Entidad.objects.get(nombre=tenant)
    except Exception:
        messages.error(request, "Error: La entidad solicitada no existe")
        return redirect('listar_dirigentes_nacionales')

    connection.set_tenant(entidad)
    ContentType.objects.clear_cache()
    try:
        dirigente = Dirigente.objects.get(id=id_dirigente)
    except Dirigente.DoesNotExist:
        messages.error(request, 'El dirigente que desea ver no existe')
        return redirect('listar_dirigentes_nacionales')

    funciones = Funcion.objects.filter(dirigente=dirigente)

    return render(request, 'dirigentes/dirigentes_ver.html', {
        'dirigente': dirigente,
        'funciones': funciones,
        'tenant_nacional':True
    })

def ver_caf_tenantnacional(request, id_caf,tenant):
    """
    Agosto 11 /2015
    Autor: Milton Lenis

    Ver CAF en el tenant nacional
    Se identifica el tenant al que pertenece un caf y se busca
    Se obtiene la informacion general del caf desde la base de datos y se muestra

    :param request: Petición Realizada
    :type request: WSGIRequest
    :param id_caf: Llave primaria del caf
    :type id_caf: String
    :param tenant: Nombre del esquema del tenant
    :type tenant: String
    """
    try:
        entidad = Entidad.objects.get(nombre=tenant)
    except Exception:
        messages.error(request, "Error: La entidad solicitada no existe")
        return redirect('listar_cafs_nacionales')

    connection.set_tenant(entidad)
    ContentType.objects.clear_cache()
    try:
        centro = CentroAcondicionamiento.objects.get(id=id_caf)
        planes = CAPlan.objects.filter(centro=centro)
        fotos = CAFoto.objects.filter(centro=centro)
    except Exception:
        return redirect('listar_cafs_nacionales')

    return render(request, 'cafs/ver_caf.html', {
        'centro': centro,
        'planes': planes,
        'fotos': fotos,
        'tenant_nacional':True
    })

def ver_caja_tenantnacional(request, id_ccf, tenant):
    """
    Agosto 11 /2015
    Autor: Milton Lenis

    Ver CCF en el tenant nacional
    Se identifica el tenant al que pertenece un ccf y se busca
    Se obtiene la informacion general del ccf desde la base de datos y se muestra

    :param request: Petición Realizada
    :type request: WSGIRequest
    :param id_ccf: Llave primaria del ccf
    :type id_ccf: String
    :param tenant: Nombre del esquema del tenant
    :type tenant: String
    """
    try:
        entidad = Entidad.objects.get(nombre=tenant)
    except Exception:
        messages.error(request, "Error: La entidad solicitada no existe")
        return redirect('listar_cajas_nacionales')

    connection.set_tenant(entidad)
    ContentType.objects.clear_cache()
    try:
        ccf = CajaCompensacion.objects.get(id=id_ccf)
    except Exception:
        messages.error(request, "Error: La caja de compensación no existe")
        return redirect('listar_cajas_nacionales')
    horarios = HorarioDisponibilidadCajas.objects.filter(caja_compensacion=id_ccf)
    tarifas = Tarifa.objects.filter(caja_compensacion=id_ccf)
    contactos = ContactoCajas.objects.filter(caja_compensacion=id_ccf)

    return render(request, 'cajas_compensacion/ver_ccf.html', {
        'ccf': ccf,
        'horarios': horarios,
        'tarifas': tarifas,
        'contactos': contactos,
        'tenant_nacional': True
    })

