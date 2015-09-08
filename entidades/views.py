import os
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from entidades.models import *
from entidades.forms import *
from django.conf import settings
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.db import connection
from snd.modelos.personal_apoyo import *
from snd.modelos.escenarios import *
from snd.modelos.deportistas import *
from snd.modelos.cafs import *
from snd.modelos.cajas_compensacion import *
from snd.modelos.dirigentes import *
from coldeportes.utilities import calculate_age


@login_required
def tipo(request):
    return render(request, 'entidad_tipo.html', {
    })

def obtenerFormularioTenant(tipo, post=None, instance=None):
    if tipo == '1':
        nombre = 'Liga'
        form = LigaForm(post, instance=instance)
    elif tipo == '2':
        nombre = 'Federación'
        form = FederacionForm(post, instance=instance)
    elif tipo == '3':
        nombre = 'Club'
        form = ClubForm(post, instance=instance)
    elif tipo == '4':
        nombre = 'Caja de Compensación'
        form = CajaDeCompensacionForm(post, instance=instance)
    elif tipo == '5':
        nombre = 'Ente'
        form = EnteForm(post, instance=instance)
    elif tipo == '6':
        nombre = 'Comité'
        form = ComiteForm(post, instance=instance)
    elif tipo == '7':
        nombre = 'Federación Paralimpica'
        form = FederacionParalimpicaForm(post,instance=instance)
    elif tipo == '8':
        nombre = 'Liga Paralimpica'
        form = LigaParalimpicaForm(post,instance=instance)

    return [nombre, form]

@login_required
def obtenerTenant(request, idEntidad, tipo):
    if tipo == '1':
        return Liga.objects.get(id=idEntidad)
    elif tipo == '2':
        return Federacion.objects.get(id=idEntidad)
    elif tipo == '3':
        return Club.objects.get(id=idEntidad)
    elif tipo == '4':
        return CajaDeCompensacion.objects.get(id=idEntidad)
    elif tipo == '5':
        return Ente.objects.get(id=idEntidad)
    elif tipo == '6':
        return Comite.objects.get(id=idEntidad)
    elif tipo == '7':
        return FederacionParalimpica.objects.get(id=idEntidad)
    raise Exception

@login_required
def registro(request, tipo, tipoEnte=None):
    nombre, form = obtenerFormularioTenant(tipo)

    form2 = ActoresForm(tipo=tipo)

    dominio = settings.SUBDOMINIO_URL

    if request.method == 'POST':
        nombre, form = obtenerFormularioTenant(tipo, request.POST)
        #form = EntidadForm(request.POST)
        form2 = ActoresForm(request.POST)
        if form.is_valid() and form2.is_valid():
            actores = form2.save()
            if tipo == '4':
                actores.cajas = True
                actores.save()

            pagina = form.cleaned_data['pagina']
            obj = form.save(commit=False)
            obj.schema_name = pagina
            obj.domain_url = pagina + dominio
            obj.actores = actores
            obj.tipo = tipo
            if tipo == '5':
                obj.tipo_ente = tipoEnte
            if tipo == '6':
                obj.tipo_comite = tipoEnte
            try:
                obj.save()
                messages.success(request, ("%s registrado correctamente.")%(nombre))
                return redirect('entidad_registro', tipo)
            except Exception as e:
                form.add_error('pagina', "Por favor ingrese otro URL dentro del SIND")
                actores.delete()

    return render(request, 'entidad_registro.html', {
        'nombre': nombre,
        'form': form,
        'form2': form2,
        'dominio': dominio
    })

@login_required
def editar(request, idEntidad, tipo):
    try:
        instance = obtenerTenant(request, idEntidad, tipo)
    except Exception:
        return redirect('entidad_listar')

    nombre, form = obtenerFormularioTenant(tipo, instance=instance)
    form2 = ActoresForm(instance=instance.actores, tipo=tipo)

    if request.method == 'POST':
        nombre, form = obtenerFormularioTenant(tipo, post=request.POST, instance=instance)
        form2 = ActoresForm(request.POST, instance=instance.actores)
        if form.is_valid() and form2.is_valid():
            actores = form2.save()
            if tipo == '4':
                actores.cajas = True
                actores.save()
            obj = form.save()
            messages.success(request, ("%s editado correctamente.")%(nombre))
            return redirect('entidad_listar')

    return render(request, 'entidad_editar.html', {
        'nombre': nombre,
        'form': form,
        'form2': form2,
    })

@login_required
def listar(request):
    entidades = Entidad.objects.exclude(schema_name="public")
    return render(request, 'entidad_listar.html', {
        'entidades': entidades,
    })


from django.contrib.contenttypes.models import ContentType
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import connection

@csrf_exempt
def appMovilLogin(request):
    from django.contrib.auth.models import User
    from django.contrib.auth import authenticate, login

    if request.method == 'GET':
        username = request.GET['name']
        password = request.GET['pw']
        entidad = request.GET['entidad']

        entidad = Entidad.objects.get(schema_name=entidad)
        connection.set_tenant(entidad)

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                return JsonResponse({'id': user.id})

    return JsonResponse({'id': None})

from snd.modelos.cafs import *
from snd.modelos.escenarios import *
def appMovilObtenerActores(request):
    datos = {'escenarios':[], 'cafs':[]} # [Escenarios, CAFS]
    if request.method == 'GET':
        entidad = request.GET.get('entidad')
        entidad = Entidad.objects.get(schema_name=entidad)
        connection.set_tenant(entidad)
        centros = CentroAcondicionamiento.objects.all()
        
        for i in centros:
            dato = {
                'id': i.id,
                'nombre': i.nombre,
                'latitud': i.latitud,
                'longitud': i.longitud,
                'altura': i.altura,
                'sincronizar': False,
            }
            datos['cafs'].append(dato)

        escenarios = Escenario.objects.all()
        for i in escenarios:
            dato = {
                'id': i.id,
                'nombre': i.nombre,
                'latitud': i.latitud,
                'longitud': i.longitud,
                'altura': i.altura,
                'sincronizar': False,
            }
            datos['escenarios'].append(dato)

    return JsonResponse(datos)

def actualizarLocalizacionActor(actor, modelo):
    instancia = modelo.objects.get(id=actor['id'])
    instancia.latitud = actor['latitud']
    instancia.longitud = actor['longitud']
    instancia.altura = actor['altura']
    instancia.save()

import json
def appMovilActualizarLocalizacion(request):
    if request.method == 'GET':
        entidad = request.GET['entidad']
        entidad = Entidad.objects.get(schema_name=entidad)
        connection.set_tenant(entidad)

        tipoActor = request.GET['tipoActor']
        actor = json.loads(request.GET['actor'])

        if tipoActor == '1':
            actualizarLocalizacionActor(actor, CentroAcondicionamiento)
            return JsonResponse({'response': True})

        if tipoActor == '0':
            actualizarLocalizacionActor(actor, Escenario)
            return JsonResponse({'response': True})

def appMovilSincronizar(request):
    if request.method == 'GET':
        entidad = request.GET.get('entidad')
        entidad = Entidad.objects.get(schema_name=entidad)
        connection.set_tenant(entidad)

        escenarios = json.loads(request.GET.get('escenarios', '[]'))
        cafs = json.loads(request.GET.get('cafs', '[]'))

        for i in cafs:
            actualizarLocalizacionActor(i, CentroAcondicionamiento)

        for i in escenarios:
            actualizarLocalizacionActor(i, Escenario)

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


def listar_personal_apoyo_nacionales(request):
    return render(request,'tenant_nacional/personal_apoyo_listar.html',{})

def listar_dirigentes_nacionales(request):
    return render(request,'tenant_nacional/dirigentes_listar.html',{})

def listar_deportistas_nacionales(request):
    return render(request,'tenant_nacional/deportistas_listar.html',{})

def listar_escenarios_nacionales(request):
    return render(request,'tenant_nacional/escenarios_listar.html',{})

def listar_cajas_nacionales(request):
    return render(request,'tenant_nacional/cajas_listar.html',{})

def listar_cafs_nacionales(request):
    return render(request,'tenant_nacional/cafs_listar.html',{})

def ver_personal_apoyo_tenantnacional(request, id_personal_apoyo, tenant):
    """
    Agosto 11 /2015
    Autor: Milton Lenis

    Ver Personal de apoyo en el tenant nacional
    Se identifica el tenant al que pertenece un personal de apoyo y se busca
    Se obtiene la informacion general del personal de apoyo desde la base de datos y se muestra

    :param request: Petición Realizada
    :type request: WSGIRequest
    :param id_personal_apoyo: Llave primaria del personal de apoyo
    :type id_personal_apoyo: String
    :param tenant: Nombre del esquema del tenant
    :type tenant: String
    """
    try:
        entidad = Entidad.objects.get(nombre=tenant)
    except Exception:
        messages.error(request, "Error: La entidad solicitada no existe")
        return redirect('listar_personal_apoyo_nacionales')

    connection.set_tenant(entidad)
    ContentType.objects.clear_cache()
    try:
        personal_apoyo = PersonalApoyo.objects.get(id=id_personal_apoyo)
    except:
        messages.error(request, "Error: No existe el personal de apoyo solicitado o su información es incompleta")
        return redirect('listar_personal_apoyo_nacionales')
    formacion_deportiva = FormacionDeportiva.objects.filter(personal_apoyo=personal_apoyo)
    experiencia_laboral = ExperienciaLaboral.objects.filter(personal_apoyo=personal_apoyo)
    personal_apoyo.edad = calculate_age(personal_apoyo.fecha_nacimiento)

    return render(request,'personal_apoyo/ver_personal_apoyo.html',{
            'personal_apoyo':personal_apoyo,
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

