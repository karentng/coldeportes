from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
import os
from snd.formularios.dirigentes  import *


def crearDirigente(request):
    return("Hola Dirigentes Nuevo")


def listarDirigentes(request):
    return("Hola Dirigentes Lista")