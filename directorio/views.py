from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from directorio.forms import *
from directorio.models import *
from snd.models import *
from django.db import connection

def crear_vista(sql):
    cursor = connection.cursor()
    r=''
    r=cursor.execute(sql)
    r=connection.commit()
    return r

def buscar_contenido(actor, texto, listado_resultados):
    if actor=='ES':
        listado_resultados.append(EscenarioView.objects.filter(contenido__icontains=texto).distinct('nombre'))
    if actor=='CA':
        listado_resultados.append(CAFView.objects.filter(contenido__icontains=texto).distinct('nombre'))

    return listado_resultados

def agregar_grupo(resultados):
    for resultado in resultados:
        for objeto in resultado:
            objeto.grupo=objeto.__class__.__name__


@login_required
def directorio_buscar(request):
    """
    Julio 22 / 2015
    Autor: Karent Narvaez Grisales
    
    realizar búsqueda de los diferentes criterios para un contacto en el directorio.

    Se obtienen los escenario que ha registrado el tenant que realiza la petición

    :param request:   Petición realizada
    :type request:    WSGIRequest
    """
    
    #esto se va a leer de un archivo, por ahora está así para pruebas
    sql = "create or replace view directorio_escenarioview as select  E.id, E.nombre,E.direccion, E.latitud,  E.longitud, E.altura,  E.ciudad_id, E.comuna, E.barrio, E.estrato, E.nombre_administrador, E.entidad_id, E.estado, C.nombre as nombre_contacto, C.telefono as telefono_contacto, C.email as email_contacto,  C.descripcion as descripcion_contacto, H.id as horario_id, H.hora_inicio,  H.hora_fin,  HD.dias_id,  H.descripcion as descripcion_horario,  F.foto,  E.nombre||' '||E.barrio||' ' ||E.estrato||' '||EN.nombre as contenido from snd_escenario E LEFT join snd_contacto C on C.escenario_id=E.id  LEFT join snd_horariodisponibilidad H on H.escenario_id=E.id LEFT join snd_horariodisponibilidad_dias HD on HD.horariodisponibilidad_id=H.id LEFT join snd_foto F on F.escenario_id=E.id  LEFT join public.entidades_entidad EN on E.entidad_id=EN.id; create or replace view directorio_cafview as select  CAF.id, CAF.nombre, CAF.direccion, CAF.latitud, CAF.longitud, CAF.telefono, CAF.altura, CAF.email, CAF.web, CAF.ciudad_id, CAF.comuna, CAF.barrio, CAF.estrato, CAF.nombre_administrador, CAF.entidad_id, CAF.estado, CF.foto, CAF.nombre||' '||CAF.email||' '||CAF.barrio|| ' '||CAF.estrato||' '||CAF.email||' '|| CAF.nombre_administrador||' '||EN.nombre as contenido from snd_centroacondicionamiento CAF LEFT join snd_cafoto CF on CF.centro_id=CAF.id LEFT join public.entidades_entidad EN on CAF.entidad_id=EN.id"
    resultado = crear_vista(sql)
    #print(resultado)

    form = DirectorioBusquedaForm()

    #inicialización de variables resultados
    listado_resultados =[]

    if request.method == 'POST':

        form = DirectorioBusquedaForm(request.POST)

        if form.is_valid():
            ciudades = request.POST.getlist('ciudad') or None
            actores = request.POST.getlist('actor') or None
            texto = request.POST.get('texto_a_buscar') or ''

            if actores==None and ciudades==None:
                listado_resultados.append(EscenarioView.objects.filter(contenido__icontains=texto).distinct('nombre'))
            elif actores==None and ciudades!=None:
                for ciudad in ciudades:
                    listado_resultados.append(EscenarioView.objects.filter(contenido__icontains=texto, ciudad=ciudad).distinct('nombre'))
            elif actores!=None and ciudades==None:
                for actor in actores:                    
                    listado_resultados = buscar_contenido(actor, texto, listado_resultados)
            
            agregar_grupo(listado_resultados)  
            print(listado_resultados)

    #print(listado_resultados)

    return render(request, 'directorio_buscar.html', {
        'form': form,
        'listado_resultados': listado_resultados,
        #'cafs': cafs,
    })