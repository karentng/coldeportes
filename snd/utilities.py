from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from datetime import date

def all_permission_required(*perms):
    return user_passes_test(lambda u: all(u.has_perm(perm) for perm in perms))

def any_permission_required(*perms):
    return user_passes_test(lambda u: any(u.has_perm(perm) for perm in perms))

def superuser_only(function):
    def _inner(request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('login')
        return function(request, *args, **kwargs)
    return _inner

def adicionarClase(campo, clase):
    campo.widget.attrs.update({'class': clase})
    if clase == 'fecha':
        campo.widget.attrs.update({'readonly': True})
    return campo

def calculate_age(born):
    """
    Junio 22 / 2015
    Autor: Daniel Correa

    Funcion para el calculo de la edad de acuerdo a una fecha ingresada por parametro
    :param born: Fecha de nacimiento de la persona a calcular edad
    :type born: Datetime.date
    """

    today = date.today()
    try:
        birthday = born.replace(year=today.year)
    except ValueError: # caso de  February 29 en año no bisiesto
        birthday = born.replace(year=today.year, month=born.month+1, day=1)
    if birthday > today:
        return today.year - born.year - 1
    else:
        return today.year - born.year