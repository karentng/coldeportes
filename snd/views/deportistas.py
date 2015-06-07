from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from formtools.wizard.views import SessionWizardView
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
import os
from snd.formularios.deportistas  import *
from snd.models import *
from entidades.models import *
from django.contrib import messages

def crear_deportista(request):
    return redirect('/escenarios/listar')

def desactivar_deportista(request):
    return redirect('/escenarios/listar')

def listar_deportista(request):
    return redirect('/escenarios/listar')