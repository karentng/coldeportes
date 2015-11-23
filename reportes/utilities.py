"""
    Noviembre 23, 2015
    Autor: Milton Lenis

    Esta función se utiliza para organizar los datos obtenidos de las consultas con los nombres respectivos de las
    categorías
"""
def sumar_datos_diccionario(datos, choices):
    diccionario_inicial = crear_diccionario_inicial(choices)
    valores_choices = convert_choices_to_array(choices)

    for temp_dict in datos:
        diccionario_inicial[temp_dict['descripcion']] += temp_dict['cantidad']

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
