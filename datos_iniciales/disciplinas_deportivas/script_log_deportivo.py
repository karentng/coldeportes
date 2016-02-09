from entidades.models import Entidad
from snd.modelos.deportistas import HistorialDeportivo
from django.db import connection

def create_log_deportivo():
	"""
	Febrero 9, 2016
	Autor: Daniel Correa

	Permite crear un log con la informacion de los historiales deportivos y limpiar su informacion en la db
	"""
	file = open('datos_iniciales/disciplinas_deportivas/log_deportivo.txt', 'w+')
	entidades = Entidad.objects.exclude(nombre='publico')
	for e in entidades:
		connection.set_tenant(e)
		historiales = HistorialDeportivo.objects.all()
		for h in historiales:
			if h.modalidad or h.prueba or h.categoria:	
				file.write(
					'{Entidad:' + str(e.nombre) +
					'\n Id Entidad:' + str(e.id) + 
					'\n Deportista:' + str(h.deportista.full_name()) +
					'\n Id Deportista:' + str(h.deportista.id) + 
					'\n Historial:' + str(h.nombre) + 
					'\n Id Historial:' + str(h.id) +
					'\n Prueba:' + str(h.prueba) + 
					'\n Modalidad:' + str(h.modalidad) +
					'\n Categoria:' + str(h.categoria) +
					'}\n \n')
			h.modalidad = ''
			h.categoria = ''
			h.prueba = ''
			h.save()
	file.close()
	print('log creado exitosamente en datos_iniciales/disciplinas_deportivas/log_deportivo.txt')

create_log_deportivo()