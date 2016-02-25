"""
    Enero 24, 2016
    Autor: Daniel Correa

    Esta funcion permite conocer la fecha de nacimiento maxima dada una edad y el dia en curso
"""
from reportes.forms import VISUALIZACIONES


def fecha_nacimiento_maxima(edades):
    from datetime import date
    hoy = date.today()
    result = []
    for edad in edades:
        maximo = hoy.replace(year=hoy.year-edad)
        result.append(maximo)
    return result

"""
    Noviembre 23, 2015
    Autor: Milton Lenis

    Esta función se utiliza para organizar los datos obtenidos de las consultas con los nombres respectivos de las
    categorías
"""
def sumar_datos_diccionario(datos, choices):
    choices = choices + (('nr', 'NO REGISTRA'),)
    diccionario_inicial = crear_diccionario_inicial(choices)
    valores_choices = convert_choices_to_array(choices)

    if choices[0][0] != 0 and isinstance(choices[0][0],int):
        valores_choices = ['Comodin'] + valores_choices

    for temp_dict in datos:
        if temp_dict['descripcion'] != None:
            diccionario_inicial[temp_dict['descripcion']] += temp_dict['cantidad']
        else:
            diccionario_inicial['nr'] += temp_dict['cantidad']

    dict_con_choices = {}
    for key in diccionario_inicial:
        try:
            nueva_llave = valores_choices[key]
        except Exception:
            nueva_llave = obtener_nueva_llave(key,choices)
        dict_con_choices[nueva_llave] = diccionario_inicial[key]
    return dict_con_choices


"""
    Noviembre 23, 2015
    Autor: Milton Lenis

    Función auxiliar para obtener una llave cuando el campo no es numérico en el choices
"""
def obtener_nueva_llave(key,choices):
    for llave,valor in choices:
        if llave == key:
            return valor
    raise Exception

"""
    Noviembre 23, 2015
    Autor: Milton Lenis

    Función para convertir los choices del modelo en arreglo con los valores en string
"""
def convert_choices_to_array(tuple):
    return [cadena for numero,cadena in tuple]


"""
    Noviembre 23, 2015
    Autor: Milton Lenis

    Método para crear el diccionario inicial con base en el choices obtenido del modelo
"""
def crear_diccionario_inicial(tuple):
    temp_dict = {}
    for numero,cadena in tuple:
        temp_dict[numero] = 0
    return temp_dict


"""
    Febrero 8, 2016
    Autor: Milton Lenis

    Método auxiliar para obtener los datos necesarios para georreferenciación de los escenarios y caf (Aunque funciona de manera genérica)
    de las vistas de un determinado tenant

    :param view = Vista de donde se extraerán los objetos

"""
def atributos_actor_vista(view):
    todos_actores = view.objects.filter(estado=0).order_by('id','entidad').distinct('id','entidad')
    actores = []
    for actor in todos_actores:
        actores.append(actor.obtener_atributos())
    return actores


def add_visualizacion(field, visualizaciones_definidas):
    visualizaciones = tuple()
    if visualizaciones_definidas:
        for i in VISUALIZACIONES:
            if i[0] in visualizaciones_definidas:
                visualizaciones += (i,)
        field.choices = visualizaciones


def puede_ver_reporte(actor):
    """
    Febrero 17 / 2016
    Autor: Milton Lenis

    Función para verificar en las URL si una entidad puede ver un actor para así mismo habilitar las url de reportes.
    :param actor:  Actor que se verificará
    :type actor:   String
    :returns:      Redirección a la página 403 (No tenía permisos) o a la página deseada (Si tenía permisos)
    :rtype:        HttpResponseRedirect
    """
    from django.core.exceptions import PermissionDenied
    from django.contrib.auth.models import Group

    def decorator(a_view):
        def _wrapped_view(request, *args, **kwargs):
            try:
                permisos = Group.objects.get(name="Solo lectura").permissions.all()
                permisos_text = []
                for permiso in permisos:
                    permisos_text.append(permiso.codename)
                if 'view_'+actor in permisos_text or request.tenant.schema_name == 'public':
                    return a_view(request, *args, **kwargs)
                else:
                    raise PermissionDenied
            except Group.DoesNotExist:
                raise PermissionDenied
        return _wrapped_view
    return decorator