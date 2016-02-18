from entidades.models import Entidad
from snd.modelos.deportistas import HistorialDeportivo
from django.db import connection


def create_log_deportivo():
    """
	Febrero 9, 2016
	Autor: Daniel Correa

	Permite crear un log con la informacion de los historiales deportivos y limpiar su informacion en la db
	"""
    # file = open('datos_iniciales/disciplinas_deportivas/log_deportivo.txt', 'w+')
    entidades = Entidad.objects.exclude(schema_name='public')
    array = {}
    i = 0
    for e in entidades:
        connection.set_tenant(e)
        historiales = HistorialDeportivo.objects.all()
        for h in historiales:
            if h.modalidad or h.prueba or h.categoria:
                array[i] = {'Entidad': str(e.nombre),
                        'Id Entidad' : str(e.id) ,
                        'Deportista' : str(h.deportista.full_name()) ,
                        'Id Deportista' : str(h.deportista.id) ,
                        'Historial' : str(h.nombre) ,
                        'Id Historial' : str(h.id) ,
                        'Prueba' : str(h.prueba) ,
                        'Modalidad' :str(h.modalidad) ,
                        'Categoria' : str(h.categoria)
                        }
                i+=1
    #file.close()
    print('log creado exitosamente en datos_iniciales/disciplinas_deportivas/log_deportivo.txt')
    return array
