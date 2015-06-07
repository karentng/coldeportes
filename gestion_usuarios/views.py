from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from gestion_usuarios.forms import *
from django.contrib.auth.models import *

def inicio(request):
    digitador = None

    grupos = Group.objects.all()
    if len(grupos) == 0:
        digitador = Group(name='Digitador')
        digitador.save()
        Group(name='Solo lectura').save()

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
            return redirect('listar_escenarios')

    return redirect('login')

@login_required
def crear(request):
    form = UserForm()

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            obj = form.save()
            grupo = form.cleaned_data['grupo']
            grupo.user_set.add(obj)
            request.session['usuario_creado'] = True
            return redirect('usuarios_lista')
    else:
        try:
            creado = request.session.get('usuario_creado')
            del request.session['usuario_creado']
        except Exception:
            creado = None

    return render(request, 'usuarios_crear.html', {
        'form': form,
        'creado': creado,
    })

@login_required
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
            return redirect('usuarios_lista')

    return render(request, 'usuarios_modificar.html', {
        'form': form,
    })

@login_required
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
                return redirect('usuarios_lista')
            

    return render(request, 'usuarios_password.html', {
        'form': form,
        'usuario': usuario,
    })

@login_required
def lista(request):
    usuarios = User.objects.all()
    return render(request, 'usuarios_lista.html', {
        'usuarios': usuarios,
    })