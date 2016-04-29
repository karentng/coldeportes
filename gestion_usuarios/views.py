from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from gestion_usuarios.forms import *
from django.contrib.auth.models import *
from django.contrib import messages
from coldeportes.utilities import superuser_only,calculate_age
from snd.models import PersonalApoyo
from snd.modelos.deportistas import Deportista
from snd.modelos.escenarios import Escenario,CaracterizacionEscenario
from normograma.models import Norma
from transferencias.models import Transferencia
from django.db import connection
from django.contrib.contenttypes.models import ContentType
from gestion_usuarios.models import PERMISOS_DIGITADOR, PERMISOS_LECTURA
from django.db.models import Q
from coldeportes.utilities import permisosPermitidos
from directorio.models import *
from noticias.models import Noticia
from entidades.models import Entidad
from reportes.utilities import atributos_actor_vista
from django.http import HttpResponse


def cambiarNombreDePermisos():
    permisos = Permission.objects.filter(
        Q(name__icontains='Can delete')|
        Q(name__icontains='Can add')|
        Q(name__icontains='Can change')
    )
    for i in permisos:
        nombre_permiso = i.name
        if 'Can delete' in nombre_permiso:
            nombre_permiso = nombre_permiso.replace('Can delete', 'Permite eliminar')
        elif 'Can add' in nombre_permiso:
            nombre_permiso = nombre_permiso.replace('Can add', 'Permite crear')
        elif 'Can change' in nombre_permiso:
            nombre_permiso = nombre_permiso.replace('Can change', 'Permite editar')
        i.name = nombre_permiso
        i.save()

def asignarPermisosGrupo(request, grupo, permisos):
    permisos = permisosPermitidos(request, permisos)
    permisos = Permission.objects.filter(codename__in=permisos)
    #si se ha quitado un actor a la entidad se quita de sus permisos
    actual = grupo.permissions.all()
    for permiso in actual:#la cantidad de permisos son pocos, no creo que el for impacte mucho
        if permiso not in permisos:
            grupo.permissions.remove(permiso)
    for permiso in permisos:
        try:
            grupo.permissions.add(permiso)
        except Exception as e:
            print(e)
            print('Ha ocurrido un error al actulizar los permisos de escritura')

def asignarPermisosGrupoLectura(request, grupo, permisos):
    #agrega los permisos de lectura que son obligatorios, tenga o no el actor
    tipo = request.tenant.tipo
    if tipo == 5:
        tipoEnte = request.tenant.ente.tipo_ente
    elif tipo == 6:
        tipoEnte = request.tenant.comite.tipo_comite
    else:
        tipoEnte = 0
    try:
        actores = Permisos.objects.get(entidad=tipo,tipo=tipoEnte).get_actores('%')
    except Permisos.DoesNotExist:
        messages.error(request,'La entidad actual no tiene permisos de lectura')
    else:
        permitidos = []
        for permiso,actor in permisos:
            if actor in actores:
                permitidos.append(permiso)
        permisos = Permission.objects.filter(codename__in=permitidos)
        for permiso in permisos:
            try:
                grupo.permissions.add(permiso)
            except Exception as e:
                print('Ha ocurrido un error al actualizar los permisos de lectura')
                print(e)


"""
Autor: Milton Lenis
Fecha: 3 Febrero 2016


NOTA: En esta vista se crea un fix para los actores de aquellas entidades que se crearon antes de crear la funcionalidad
de permisos que hizo Cristian, NO ES NECESARIO QUE LA USEN PARA SUS ENTORNOS DE DESARROLLO LOCALES ES SOLO PARA ACOMODAR
LOS SERVIDORES.
"""
def fix_actores_entidades(request):
    from coldeportes.utilities import obtener_modelo_actor

    entidades = Entidad.objects.exclude(schema_name='public')
    for entidad in entidades:
        entidad = entidad.obtenerTenant()
        if entidad.tipo == 5:
            tipo_sub_entidad = entidad.tipo_ente
        elif entidad.tipo == 6:
            tipo_sub_entidad = entidad.tipo_comite
        else:
            tipo_sub_entidad = 0

        tipo_entidad = entidad.tipo

        permisos = Permisos.objects.get(tipo=tipo_sub_entidad,entidad=tipo_entidad)

        for actor_false in permisos.get_actores('--'):
            setattr(entidad.actores,actor_false,False)
            entidad.save()
            entidad.actores.save()

        for actor_true in permisos.get_actores('O'):
            setattr(entidad.actores,actor_true,True)
            entidad.save()
            entidad.actores.save()

        #Se comenta para que no se siga intentando borrar ya que no es necesario
        #modelos_a_borrar = [obtener_modelo_actor(actor) for actor in permisos.get_actores('--')]
        connection.set_tenant(entidad)
        request.tenant = entidad

        ##Se comenta para que no se siga intentando borrar ya que no es necesario
        """
        for modelo in modelos_a_borrar:
            try:
                modelo.objects.all().delete()
            except Exception as e:
                print(e)
        """

        try:
            #si llegan a editar el nombre del grupo, tendremos un error
            digitador = Group.objects.get(name="Digitador")
            lectura = Group.objects.get(name='Solo lectura')
        except Group.DoesNotExist:
            digitador = None
            lectura = None

        if digitador and lectura:#sólo si se encuentran los grupos se actualizan sus permisos
            asignarPermisosGrupo(request, digitador, PERMISOS_DIGITADOR)
            asignarPermisosGrupo(request, lectura, PERMISOS_LECTURA)
            asignarPermisosGrupoLectura(request, digitador, PERMISOS_LECTURA)
            asignarPermisosGrupoLectura(request, lectura, PERMISOS_LECTURA)

        connection.set_schema_to_public()
        request.tenant = Entidad.objects.get(schema_name='public')

    return HttpResponse("Se han actualizado las entidades del servidor correctamente")

"""
------------------------------------------------------------------------------------------------------------------------
"""

def inicio(request):
    schema_name = request.tenant.schema_name

    digitador = None
    lectura = None
    grupos = Group.objects.all()
    cambiarNombreDePermisos()
    if len(grupos) == 0:
        digitador = Group(name='Digitador')
        digitador.save()
        lectura = Group(name='Solo lectura')
        lectura.save()
    else:
        try:
            #si llegan a editar el nombre del grupo, tendremos un error
            digitador = Group.objects.get(name="Digitador")
            lectura = Group.objects.get(name='Solo lectura')
        except Group.DoesNotExist:
            pass
    if digitador and lectura:#sólo si se encuentran los grupos se actualizan sus permisos
        asignarPermisosGrupo(request, digitador, PERMISOS_DIGITADOR)
        asignarPermisosGrupo(request, lectura, PERMISOS_LECTURA)
        asignarPermisosGrupoLectura(request, digitador, PERMISOS_LECTURA)
        asignarPermisosGrupoLectura(request, lectura, PERMISOS_LECTURA)

    superUsuarios = User.objects.filter(is_superuser=True)
    if len(superUsuarios) == 0:
        if schema_name == 'public':
            password = "cedesoft"
        else:
            password = ("%s-%s")%("root", schema_name)
        user = User.objects.create_user('root', 'root@gmail.com', password)
        user.first_name = 'Administrador'
        user.is_superuser = True
        user.is_staff = True
        user.save()
        digitador.user_set.add(user)

    entidades = Entidad.objects.all()
    if len(entidades) == 1:#sólo debería de existir la entidad pública
        actores1 = Actores(centros=False,escenarios=False,deportistas=False,personal_apoyo=True,dirigentes=True,cajas=False,selecciones=True, centros_biomedicos=False, normas=False, escuelas_deportivas=False, noticias=True)
        actores1.save()
        actores2 = Actores(centros=False,escenarios=False,deportistas=False,personal_apoyo=True,dirigentes=True,cajas=False,selecciones=True, centros_biomedicos=False, normas=False, escuelas_deportivas=False, noticias=True)
        actores2.save()
        ciudad = Ciudad.objects.get(id=109)#bogotá
        comiteOlimpico = Comite(tipo=6,tipo_comite=1,nombre="Comité Olímpico Colombiano",direccion="Av. 68 # 55-65",pagina_web="http://www.coc.org.co/",telefono="571 6300093",actores=actores1,ciudad=ciudad)
        comiteOlimpico.schema_name = 'coc'
        comiteOlimpico.domain_url = 'coc' + settings.SUBDOMINIO_URL
        comiteOlimpico.save()
        comiteParalimpico = Comite(tipo=6,tipo_comite=2,nombre="Comité Paralímpico Colombiano",direccion="Calle 63 # 59a-06",pagina_web="http://comiteparalimpicocolombiano.org/",telefono="571 2319729",actores=actores2,ciudad=ciudad)
        comiteParalimpico.schema_name = 'cpc'
        comiteParalimpico.domain_url = 'cpc' + settings.SUBDOMINIO_URL
        comiteParalimpico.save()


    if schema_name == 'public':
        return redirect('inicio_public')
    else:
        return redirect('inicio_tenant')


def inicio_public(request):
    from entidades.modelos_vistas_reportes import PublicDeportistaView, PublicEscenarioView
    from reportes.utilities import atributos_actor_vista
    from django.db.models import Count

    import json
    import datetime

    ubicaciones = atributos_actor_vista(PublicEscenarioView)
    cantidad_deportistas = PublicDeportistaView.objects.filter(estado__in=[0,2]).order_by('id','entidad').distinct('id','entidad').count()
    cantidad_escenarios = PublicEscenarioView.objects.filter(estado=0).order_by('id','entidad').distinct('id','entidad').count()

    cantidad_entes = list(Entidad.objects.exclude(schema_name='public').values('tipo').order_by().annotate(Count('tipo')))
    for i in range(0, len(cantidad_entes)):
        cantidad_entes[i]['tipo'] = TIPOS[cantidad_entes[i]['tipo']-1][1]

    tipoTenant = request.tenant.obtenerTenant()
    posicionInicial = tipoTenant.posicionInicialMapa()

    try:
        noticias_todas = Noticia.objects.filter(Q(fecha_inicio__lte=datetime.date.today()) &
                                                Q(fecha_expiracion__gte=datetime.date.today()),
                                                estado=1).order_by("-fecha_inicio")
        if len(noticias_todas) > 5:
            noticias = noticias_todas[:5]
        else:
            noticias = noticias_todas
    except Exception:
        noticias = []

    return render(request, 'index_public.html', {
        'deportistas': cantidad_deportistas,
        'escenarios': cantidad_escenarios,
        'cantidad_entes': json.dumps(cantidad_entes),
        'ubicaciones': json.dumps(ubicaciones),
        'posicionInicial': json.dumps(posicionInicial),
        'noticias': noticias,
    })


def tiene_reconocimiento_deportivo(club):
    from datetime import date
    """
    Abril 27 / 2016

    Autor: Karent Narvaez
    Permite verificar si un club tiene reconocimiento deportivo o no.

    :para club: club a verificar
    :type club: Object Club
    """
    if  club.fecha_vigencia < date.today():
        club.reconocimiento = False
        club.save()
        return False
    else:
        return True


def inicio_tenant(request):
    import json
    import datetime
    """
    Julio 14 / 2015
    Autor: Daniel Correa

    Index para tentat

    Esta vista permite renderizan el panel de control del tenant, donde se mostraran notificaciones y demas opciones de control

    :param request: Petición Realizada
    :type request: WSGIRequest
    """

    #Inicio consulta de transferencias
    transferencias = Transferencia.objects.filter(estado='Pendiente')
    transfer_personas = []
    usuario = request.user

    for t in transferencias:
        connection.set_tenant(t.entidad)
        ContentType.objects.clear_cache()
        objeto_trans = Deportista.objects.get(id=t.id_objeto)
        objeto_trans.procedencia = t.entidad
        objeto_trans.fecha_solicitud = t.fecha_solicitud
        objeto_trans.id_trans = t.id
        transfer_personas.append(objeto_trans)

    connection.set_tenant(request.tenant)
    ContentType.objects.clear_cache()
    #Fin consulta de transferencias

    actoresAsociados = request.tenant.cantidadActoresAsociados()
    tipoTenant = request.tenant.obtenerTenant()

    #Mejorado con uso de vistas
    from reportes.models import TenantEscenarioView
    from reportes.models import TenantCafView

    ubicaciones = atributos_actor_vista(TenantEscenarioView)
    ubicaciones = ubicaciones + atributos_actor_vista(TenantCafView)
    #--------------------------

    posicionInicial = tipoTenant.posicionInicialMapa()

    connection.set_tenant(request.tenant)
    ContentType.objects.clear_cache()
    entidad = tipoTenant.obtener_datos_entidad()

    #Se verifica si el tenant es un Club para notificar en caso de que el reconocimiento deportivo esté vencido
    if entidad['tipo_tenant'] == 'Club':
        #Verifica si tiene fecha de vigencia el club, si no la tiene entonces no ha obtenido reconocimiento deportivo previamente
        if tipoTenant.fecha_vigencia:
            vigente = tiene_reconocimiento_deportivo(tipoTenant)
            #Si el reconocimiento deportivo no está vigente se notifica al usuario si está autenticado y es digitador
            if not vigente and usuario.is_authenticated() and usuario.groups.filter(name='Digitador').exists():
                messages.warning(request, "El reconocimiento deportivo del club no se encuentra vigente.")
        else:
            messages.warning(request, "Este club no cuenta con reconocimiento deportivo.")


    if request.tenant.tipo == 3:
        entidad['planes_de_costo']= entidad['planes_de_costo'].filter(estado=0)
        entidad['socios'] = entidad['socios'].filter(estado=0)
    try:
        noticias_todas = Noticia.objects.filter(Q(fecha_inicio__lte=datetime.date.today()) &
                                                Q(fecha_expiracion__gte=datetime.date.today()),
                                                estado=1).order_by("-fecha_inicio")
        if len(noticias_todas) > 5:
            noticias = noticias_todas[:5]
        else:
            noticias = noticias_todas
    except Exception:
        noticias = []


    return render(request, 'index_tenant.html', {
        'transfer_persona': transfer_personas,
        'actoresAsociados': actoresAsociados,
        # 'actoresAsociadosJSON': json.dumps(actoresAsociados),
        'ubicaciones': json.dumps(ubicaciones),
        'posicionInicial': json.dumps(posicionInicial),
        'noticias': noticias,
        'entidad': entidad,
        'tipoTenant': tipoTenant

    })

@login_required
@superuser_only
def crear(request):
    form = UserForm()

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            obj = form.save()
            grupo = form.cleaned_data['grupo']
            grupo.user_set.add(obj)
            messages.success(request, "Usuario registrado correctamente.")
            return redirect('usuarios_lista')

    return render(request, 'usuarios_crear.html', {
        'form': form,
    })

@login_required
@superuser_only
def modificar(request, idUsuario):
    try:
        usuario = User.objects.get(id=idUsuario)
    except Exception:
        return redirect('usuarios_lista')
    
    grupo = usuario.groups.all()[0]
    form = UserModificarForm(instance=usuario, initial={'grupo': grupo})

    if request.method == 'POST':
        form = UserModificarForm(request.POST, instance=usuario, initial={'grupo': grupo})
        if form.is_valid():
            obj = form.save()
            grupo.user_set.remove(usuario)
            grupo = form.cleaned_data['grupo']
            grupo.user_set.add(obj)
            messages.success(request, "Usuario modificado correctamente.")
            return redirect('usuarios_lista')

    return render(request, 'usuarios_modificar.html', {
        'form': form,
    })

@login_required
@superuser_only
def password(request, idUsuario):
    try:
        usuario = User.objects.get(id=idUsuario)
    except Exception:
        return redirect('usuarios_lista')

    form = UserPasswordForm()
    if request.method == 'POST':
        form = UserPasswordForm(request.POST)
        if form.is_valid():
            pass1 = form.cleaned_data['password1']
            pass2 = form.cleaned_data['password2']

            if pass1 == pass2:
                usuario.set_password(pass1)
                usuario.save()
                messages.success(request, "Password cambiado correctamente.")
                return redirect('usuarios_lista')
            

    return render(request, 'usuarios_password.html', {
        'form': form,
        'usuario': usuario,
    })

@login_required
@superuser_only
def lista(request):
    usuarios = User.objects.all()
    return render(request, 'usuarios_lista.html', {
        'usuarios': usuarios,
    })

@login_required
@superuser_only
def desactivar(request, idUsuario):
    try:
        usuario = User.objects.get(id=idUsuario)
    except Exception:
        return redirect('usuarios_lista')

    usuario.is_active = not(usuario.is_active)
    usuario.save()
    if usuario.is_active == True:
        messages.success(request, "Usuario activado.")
    else:
        messages.success(request, "Usuario desactivado.")
    return redirect('usuarios_lista')

@login_required
@superuser_only
def grupos_listar(request):
    grupos = Group.objects.all()
    return render(request, 'grupos_lista.html', {
        'grupos': grupos,
    })

@login_required
@superuser_only
def grupos_crear(request):
    form = GroupForm(request=request)

    if request.method == 'POST':
        form = GroupForm(request.POST, request=request)
        if form.is_valid():
            form.save()
            messages.success(request, "Grupo creado correctamente")
            return redirect('grupos_listar')

    return render(request, 'grupos_crear.html', {
        'form': form,
    })

@login_required
@superuser_only
def grupos_modificar(request, idGrupo):
    try:
        grupo = Group.objects.get(id=idGrupo)
    except Exception:
        return redirect('grupos_listar')

    form = GroupForm(instance=grupo, request=request)
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=grupo, request=request)
        if form.is_valid():
            form.save()
            messages.success(request, "Grupo modificado correctamente")
            return redirect('grupos_listar')

    return render(request, 'grupos_modificar.html', {
        'form': form,
    })

@login_required
@superuser_only
def datos_basicos_entidad(request):
    from entidades.views import obtenerTenant, obtenerFormularioTenant

    entidad = request.tenant
    try:
        instance = obtenerTenant(request, entidad.id, str(entidad.tipo))
    except Exception as e:
        return redirect('usuarios_lista')

    nombre, form = obtenerFormularioTenant(str(entidad.tipo), instance=instance)

    if request.method == 'POST':
        nombre, form = obtenerFormularioTenant(str(entidad.tipo), post=request.POST, files=request.FILES, instance=instance)
        if form.is_valid():
            obj = form.save()
            messages.success(request, "Datos básicos editados correctamente")
            return redirect('datos_basicos_entidad')

    return render(request, 'datos_basicos_entidad.html', {
        'nombre': nombre,
        'form': form,
    })


@login_required
def fix_solicitudes_escenarios(request):
    #respuesta
    entes = Entidad.objects.filter(tipo=5)
    for e in entes:
        actores = e.actores
        actores.respuesta = True
        actores.save()

    #solicitud
    tiene_escenario = Actores.objects.filter(escenarios=True)
    for a in tiene_escenario:
        a.solicitud = True
        a.save()

    #termino
    return HttpResponse("Solicitud y Respuesta asignadas correctamente ")


@login_required
def fix_reconocimiento_deportivo(request):
    #asignar a entes actor de respuesta de reconocimiento deportivo
    entidades = Entidad.objects.filter(tipo=5)
    for entidad in entidades:
        ente = entidad.obtenerTenant()
        if ente.tipo_ente == 1:#ente municipal es tipo 1
            actores = entidad.actores
            actores.reconocimiento_respuesta = True
            actores.save()
    #asignar a clubes actor de solicitud de reconocimiento deportivo    
    clubes = Entidad.objects.filter(tipo=3)
    for club in clubes:
        actores = club.actores
        actores.reconocimiento_solicitud = True
        actores.save()

    return HttpResponse("Solicitudes y respuestas de reconocimiento deportivo asignadas correctamente")
