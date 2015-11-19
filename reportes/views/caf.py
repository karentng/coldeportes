#encoding:utf-8
from django.shortcuts import render, redirect
from django.http import JsonResponse
import ast
from reportes.forms import DemografiaForm

'''
Reportes:
    1. Dona
    2. Comparativa Horizontal
    3. Comparativa Vertical
    4. Tree Map
    5. Gráfico de cilindros
'''

def demografia(request):
    from entidades.modelos_vistas_reportes import PublicCafView
    from reportes.models import TenantCafView
    from snd.models import CentroAcondicionamiento
    from django.db.models import F, Count

    tipoTenant = request.tenant.obtenerTenant()
    
    if tipoTenant.schema_name == 'public':
        tabla = PublicCafView
    else:
        tabla = TenantCafView

    if request.is_ajax():
        '''
        departamentos = None if request.GET['departamentos'] == 'null'  else ast.literal_eval(request.GET['departamentos'])
        annos = None if request.GET['annos'] == 'null'  else ast.literal_eval(request.GET['annos'])
        
        if departamentos:
            if annos:
                centros = list()
                for anno in annos:
                    centros += tipoTenant.ejecutar_consulta(False, "list(CentroAcondicionamiento.objects.filter(ciudad__departamento__id__in=%s, fecha_creacion__gte=date(%s, 1, 1), fecha_creacion__lte=date(%s, 12, 31)).annotate(descripcion=F('ciudad__nombre')).values('descripcion').annotate(cantidad=Count('ciudad')))"%(departamentos, anno, anno))
                centros = tipoTenant.ajustar_resultado(centros)
            else:
                centros = tipoTenant.ejecutar_consulta(True, "list(CentroAcondicionamiento.objects.filter(ciudad__departamento__id__in=%s).annotate(descripcion=F('ciudad__nombre')).values('descripcion').annotate(cantidad=Count('ciudad')))"%(departamentos))
        else:
            if annos:
                centros = list()
                for anno in annos:
                    centros += tipoTenant.ejecutar_consulta(False, "list(CentroAcondicionamiento.objects.filter(fecha_creacion__gte=date(%s, 1, 1), fecha_creacion__lte=date(%s, 12, 31)).annotate(descripcion=F('ciudad__departamento__nombre')).values('descripcion').annotate(cantidad=Count('ciudad__departamento')))"%(anno, anno))
                    print (centros)
                centros = tipoTenant.ajustar_resultado(centros)
            else:
                centros = tipoTenant.ejecutar_consulta(True, "list(CentroAcondicionamiento.objects.annotate(descripcion=F('ciudad__departamento__nombre')).values('descripcion').annotate(cantidad=Count('ciudad__departamento')))")
        '''
        centros = list(tabla.objects.annotate(descripcion=F('ciudad__departamento__nombre')).values('descripcion').annotate(cantidad=Count('ciudad__departamento')))
        centros = tipoTenant.ajustar_resultado(centros)
        return JsonResponse(centros)
    else:
        #centros = tipoTenant.ejecutar_consulta(True, "list(CentroAcondicionamiento.objects.annotate(descripcion=F('ciudad__departamento__nombre')).values('descripcion').annotate(cantidad=Count('ciudad__departamento')))")

        centros = list(tabla.objects.annotate(descripcion=F('ciudad__departamento__nombre')).values('descripcion').annotate(cantidad=Count('ciudad__departamento')))
        centros = tipoTenant.ajustar_resultado(centros)
    visualizaciones = [1, 2, 3]

    form = DemografiaForm(visualizaciones=visualizaciones)
    return render(request, 'caf/demografia.html', {
        'centros': centros,
        'visualizaciones': visualizaciones,
        'form': form,
    })
'''
def generar(request):
    from django.db import connection

    sql = """
        CREATE OR REPLACE VIEW public.reportes_reportecafview AS
    """

    from entidades.models import Entidad
    entidades = Entidad.objects.all().order_by('id').values_list('schema_name', flat=True)
    primero = entidades[1]
    for i in entidades:
        if i == 'public':
            continue

        aux = ("""
            SELECT
                CAF.id, CAF.ciudad_id,
                CAF.comuna, CAF.estrato,
                CAF.latitud, CAF.longitud,
                CAF.altura, CAF.estado,
                CAF.entidad_id, CAF.fecha_creacion,
                CLASE.nombre as nombre_clase, SERVICIO.nombre as nombre_servicio
            FROM
            %s.snd_centroacondicionamiento CAF
            LEFT JOIN %s.snd_centroacondicionamiento_clases CLASES ON CLASES.centroacondicionamiento_id = CAF.id
            LEFT JOIN public.entidades_caclase CLASE ON CLASE.id = CLASES.caclase_id
            LEFT JOIN %s.snd_centroacondicionamiento_servicios SERVICIOS ON SERVICIOS.centroacondicionamiento_id = CAF.id
            LEFT JOIN public.entidades_caservicio SERVICIO ON SERVICIO.id = SERVICIOS.caservicio_id
        """)%(i, i, i)

        if primero == i:
            sql = ("%s %s")%(sql, aux)
        else:
            sql = ("%s UNION %s")%(sql, aux)
        
    sql = ("%s %s")%(sql, ";")

    cursor = connection.cursor()
    r=''
    r=cursor.execute(sql)
    r=connection.commit()
    return r

def report_caf_publico(request):
    from reportes.models import ReporteCafView
    from django.db.models import F, Count
    
    try:
        ReporteCafView.objects.all().exists()
    except Exception:
        generar(request)
    tipoTenant = request.tenant.obtenerTenant()
    centros = tipoTenant.ajustar_resultado(ReporteCafView.objects.annotate(descripcion=F('ciudad__departamento__nombre')).values('descripcion').annotate(cantidad=Count('ciudad__departamento')))
    print(centros)
    visualizaciones = [1, 2, 3]
    form = DemografiaForm(visualizaciones=visualizaciones)
    #return render(request, 'caf/report_caf_publico.html', {
    return render(request, 'caf/demografia.html', {
        'centros': centros,
        'visualizaciones': visualizaciones,
        'form': form,
    })
'''
