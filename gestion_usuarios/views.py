from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from gestion_usuarios.forms import *
from django.contrib.auth.models import *
from django.contrib import messages
from coldeportes.utilities import superuser_only,calculate_age
from snd.models import Entrenador
from snd.modelos.deportistas import Deportista
from snd.modelos.escenarios import Escenario,CaracterizacionEscenario
from transferencias.models import Transferencia
from django.db import connection
from django.contrib.contenttypes.models import ContentType

PERMISOS_DIGITADOR = [
    'add_cajacompensacion',
    'change_cajacompensacion',
    'add_dirigente',
    'change_dirigente',
    'add_deportista',
    'change_deportista',
    'add_centroacondicionamiento',
    'change_centroacondicionamiento',
    'add_entrenador',
    'change_entrenador',
    'add_escenario',
    'change_escenario',
]

def asignarPermisosGrupo(grupo, permisos):
    permisos = Permission.objects.filter(codename__in=permisos)
    for permiso in permisos:
        grupo.permissions.add(permiso)

def inicio(request):
    digitador = None

    grupos = Group.objects.all()
    if len(grupos) == 0:
        digitador = Group(name='Digitador')
        digitador.save()
        Group(name='Solo lectura').save()
        asignarPermisosGrupo(digitador, PERMISOS_DIGITADOR)

    superUsuarios = User.objects.filter(is_superuser=True)
    if len(superUsuarios) == 0:
        user = User.objects.create_user('root', 'root@gmail.com', 'root')
        user.first_name = 'Administrador'
        user.is_superuser = True
        user.is_staff = True
        user.save()
        digitador.user_set.add(user)

    if request.user.is_authenticated():
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
    """
    Julio 14 / 2015
    Autor: Daniel Correa

    Index para tentat

    Esta vista permite renderizan el panel de control del tenant, donde se mostraran notificaciones y demas opciones de control

    :param request: Petición Realizada
    :type request: WSGIRequest
    """
    transferencias = Transferencia.objects.filter(estado='Pendiente')
    transfer_personas = []
    transfer_escenarios = []
    for t in transferencias:
        entidad_cambio = t.entidad
        connection.set_tenant(entidad_cambio)
        ContentType.objects.clear_cache()
        if t.tipo_objeto=='Deportista':
            depor = Deportista.objects.get(id=t.id_objeto)
            depor.edad = calculate_age(depor.fecha_nacimiento)
            depor.procedencia = entidad_cambio
            depor.fecha_solicitud = t.fecha_solicitud
            transfer_personas.append(depor)
        elif t.tipo_objeto=='Entrenador':
            entre = Entrenador.objects.get(id=t.id_objeto)
            entre.edad = calculate_age(entre.fecha_nacimiento)
            entre.procedencia = entidad_cambio
            entre.fecha_solicitud = t.fecha_solicitud
            transfer_personas.append(entre)
        elif t.tipo_objeto=='Escenario':
            escenario = Escenario.objects.get(id=t.id_objeto)
            escenario.procedencia = entidad_cambio
            escenario.tipo = CaracterizacionEscenario.objects.get(escenario=escenario).tipo_escenario
            escenario.fecha_solicitud = t.fecha_solicitud
            transfer_escenarios.append(escenario)

    """transfer_depor = Deportista.objects.all()
    for d in transfer_depor:
        #disciplinas = ','.join(str(x) for x in d.disciplinas.all())
        #d.disciplinas_str = disciplinas
        d.edad= calculate_age(d.fecha_nacimiento)
        d.procedencia = 'Deportivo Cali'

    transfer_es = Escenario.objects.all()
    for e in transfer_es:
        e.tipo = CaracterizacionEscenario.objects.get(escenario=e).tipo_escenario
        e.procedencia= 'Deportivo Cali'"""

    return render(request,'index_tenant.html',{
        'transfer_persona' : transfer_personas,
        'transfer_escenario' : transfer_escenarios

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
    form = GroupForm()

    if request.method == 'POST':
        form = GroupForm(request.POST)
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

    form = GroupForm(instance=grupo)
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=grupo)
        if form.is_valid():
            form.save()
            messages.success(request, "Grupo modificado correctamente")
            return redirect('grupos_listar')

    return render(request, 'grupos_modificar.html', {
        'form': form,
    })