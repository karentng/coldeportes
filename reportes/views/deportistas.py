#encoding:utf-8
from django.shortcuts import render, redirect
from django.db import models
from django.http import JsonResponse
import ast

def participaciones_deportivas(request):
    """
    Reporte participaciones deportivas
    """
    #consulta que trae todas las participaciones deportiva
    '''
    {"internacional":20,...}
    []

    '''
    tipoTenant = request.tenant.obtenerTenant()
    if request.is_ajax():
        pass
    else:
        pass
