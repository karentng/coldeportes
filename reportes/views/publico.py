#encoding:utf-8
from django.shortcuts import render, redirect
from entidades.models import Permisos

def tipos(request):
    entidad = request.tenant.obtenerTenant()
    if entidad.tipo == 5:
        tipo_sub_entidad = entidad.tipo_ente
    elif entidad.tipo == 6:
        tipo_sub_entidad = entidad.tipo_comite
    else:
        tipo_sub_entidad = 0

    tipo_entidad = entidad.tipo
    permisos_permitidos_lectura = Permisos.objects.get(tipo=tipo_sub_entidad,entidad=tipo_entidad)

    actores_que_se_pueden_ver = permisos_permitidos_lectura.get_actores('%')
    actores_de_la_entidad = request.tenant.actores.resumen_nombre_atributos()

    actores_permitidos_reportes = list(set().union(actores_de_la_entidad,actores_que_se_pueden_ver))
    return render(request, 'publico/tipos.html', {'actores_permitidos_reportes':actores_permitidos_reportes
        })
