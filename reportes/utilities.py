"""
    Noviembre 23, 2015
    Autor: Milton Lenis

    Esta función se utiliza para organizar los datos obtenidos de las consultas con los nombres respectivos de las
    categorías
"""
def sumar_datos_diccionario(diccionario_inicial, datos, valores_choices):
    for temp_dict in datos:
        diccionario_inicial[temp_dict['descripcion']] += temp_dict['cantidad']

    dict_con_choices = {}
    for key in diccionario_inicial:
        nueva_llave = valores_choices[key]
        dict_con_choices[nueva_llave] = diccionario_inicial[key]
    return dict_con_choices

"""
    Noviembre 23, 2015
    Autor: Milton Lenis

    Función para convertir los choices del modelo en arreglo con los valores en string
"""
def convert_choices_to_array(tuple):
    return [cadena for numero,cadena in tuple]
