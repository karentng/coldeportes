from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from gestion_usuarios.forms import *
from django.contrib.auth.models import *
from django.contrib import messages
from coldeportes.utilities import superuser_only,calculate_age
from snd.models import PersonalApoyo
from snd.modelos.deportistas import Deportista
from snd.modelos.escenarios import Escenario,CaracterizacionEscenario
from transferencias.models import Transferencia
from django.db import connection
from django.contrib.contenttypes.models import ContentType
from gestion_usuarios.models import PERMISOS_DIGITADOR
from django.db.models import Q
from coldeportes.utilities import permisosPermitidos
from directorio.models import * 


def asignarPermisosGrupo(request, grupo, permisos):
    permisos = permisosPermitidos(request, permisos)
    permisos = Permission.objects.filter(codename__in=permisos)
    for permiso in permisos:
        grupo.permissions.add(permiso)

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

def inicio(request):
    digitador = None


    grupos = Group.objects.all()
    cambiarNombreDePermisos()
    if len(grupos) == 0:
        digitador = Group(name='Digitador')
        digitador.save()
        Group(name='Solo lectura').save()
        asignarPermisosGrupo(request, digitador, PERMISOS_DIGITADOR)

    superUsuarios = User.objects.filter(is_superuser=True)
    if len(superUsuarios) == 0:
        user = User.objects.create_user('root', 'root@gmail.com', 'root')
        user.first_name = 'Administrador'
        user.is_superuser = True
        user.is_staff = True
        user.save()
        digitador.user_set.add(user)

    entidades = Entidad.objects.all()
    if len(entidades) == 1:#sólo debería de existir la entidad pública
        actores1 = Actores(centros=True,escenarios=True,deportistas=True,personal_apoyo=True,dirigentes=True,cajas=False)
        actores1.save()
        actores2 = Actores(centros=True,escenarios=True,deportistas=True,personal_apoyo=True,dirigentes=True,cajas=False)
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

    if request.user.is_authenticated():
        # lectura y creación de vistas del directorio sql
        

        if request.tenant.schema_name == "public":
            return redirect('entidad_tipo')
        else:
            if request.user.is_superuser:
                return redirect('usuarios_lista')
            else:
                
                    
                return redirect('inicio_tenant')

    return redirect('login')

@login_required
def inicio_tenant(request):
    import json
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
    ubicaciones = tipoTenant.atributosDeSusCafs()
    ubicaciones += tipoTenant.atributosDeSusEscenarios()
    posicionInicial = tipoTenant.posicionInicialMapa()

    return render(request,'index_tenant.html',{
        'transfer_persona' : transfer_personas,
        'actoresAsociados': actoresAsociados,
        'actoresAsociadosJSON': json.dumps(actoresAsociados),
        'ubicaciones': json.dumps(ubicaciones),
        'posicionInicial': json.dumps(posicionInicial),
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