from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from directorio.forms import *
from directorio.models import EscenarioView
from snd.models import *
from django.db import connection

def crear_vista(sql):
    cursor = connection.cursor()
    r=''
    r=cursor.execute(sql)
    r=connection.commit()
    return r

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
    sql = "create or replace view directorio_escenarioview as select  E.id, E.nombre,E.direccion, E.latitud,  E.longitud, E.altura,  E.ciudad_id, E.comuna, E.barrio, E.estrato, E.nombre_administrador, E.entidad_id, E.estado, C.nombre as nombre_contacto, C.telefono as telefono_contacto, C.email as email_contacto,  C.descripcion as descripcion_contacto, H.id as horario_id, H.hora_inicio,  H.hora_fin,  HD.dias_id,  H.descripcion as descripcion_horario,  F.foto,  E.nombre||' '||E.barrio||' ' ||E.estrato||' '||EN.nombre as contenido from snd_escenario E LEFT join snd_contacto C on C.escenario_id=E.id  LEFT join snd_horariodisponibilidad H on H.escenario_id=E.id LEFT join snd_horariodisponibilidad_dias HD on HD.horariodisponibilidad_id=H.id LEFT join snd_foto F on F.escenario_id=E.id  LEFT join public.entidades_entidad EN on E.entidad_id=EN.id"
    resultado = crear_vista(sql)
    print(resultado)

    form = DirectorioBusquedaForm()

    #inicialización de variables resultados
    escenarios=[]


    if request.method == 'POST':

        form = DirectorioBusquedaForm(request.POST)

        if form.is_valid():
            ciudades = request.POST.getlist('ciudad') or None
            actores = request.POST.getlist('actor') or None
            texto = request.POST.get('texto_a_buscar') or ''

            if actores==None and ciudades==None:
                escenarios.append(EscenarioView.objects.filter(contenido__icontains=texto).distinct('nombre'))
            elif actores==None and ciudades!=None:
                for ciudad in ciudades:
                    escenarios.append(EscenarioView.objects.filter(contenido__icontains=texto, ciudad=ciudad).distinct('nombre'))
            elif actores!=None and ciudades==None:
                for actor in actores:
                    print(actor)
                    if actor=='ES':
                        print('entrooo')
                        escenarios.append(EscenarioView.objects.filter(contenido__icontains=texto).distinct('nombre'))

    #print(escenarios)

    return render(request, 'directorio_buscar.html', {
        'form': form,
        'escenarios': escenarios,
    })