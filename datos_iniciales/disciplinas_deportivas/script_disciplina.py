from entidades.models import Entidad,ModalidadDisciplinaDeportiva,TipoDisciplinaDeportiva,CategoriaDisciplinaDeportiva
from .modalidaes_categorias import modalidades,categorias
from django.db import connection
deportes = [
	'Parapentismo','Aeromodelismo','Ala delta ','Ultralivianos','Planeadores','Globos aerostáticos','Apnea',
	'Natación con aletas','Buceo','Hockey subacuático','Rugby subacuático','Pesca submarina','Orientación',
	'Automovilismo deportivo','(Automovilismo deportivo) - Rallies colombiano','(Automovilismo deportivo) - Rallie Cross',
	'(Automovilismo deportivo) - Camper Cross','(Automovilismo deportivo) - Velocidad','Ajedrez','Arquería','Bolos','Ciclismo',
	'Ecuestre','Esgrima','Esquí Náutico','Futbol','Futbol de salón','Golf','Hapkido','Karts','Motociclismo','Motonáutica','Natación',
	'Squash','Softbol','Tenis','Tenis de mesa','Voleibol','Deportes Fuerzas Armadas','Deporte montaña y escalada','Coleo','Billar',
	'Nado sincronizado','Waterpolo','Bádminton','Baloncesto','Canotaje','Balonmano','Hockey','Pentatlón moderno','Rugby','Vela','Tejo',
	'Tiro y caza','Trampolín','Triatlón'
]

def insertar_actualizar_deportes():
	"""
	Enero 30,2016
	Autor: Daniel Correa

	Permite actualizar o crear los registros de tipo disciplina deportiva sin dañar los registros existentes
	"""
	publico = Entidad.objects.get(schema_name='public')
	connection.set_tenant(publico)
	for d in deportes:
		try:
			TipoDisciplinaDeportiva.objects.get(descripcion=d)
		except Exception:
			d = TipoDisciplinaDeportiva(descripcion=d)
			d.save()

def insertar_modalidades_categorias():
	"""
	Enero 30, 2016
	Autor: Daniel Correa

	Permite insertar las modalidades y categorias de los JSON que estan en el archivo modalidades_categorias.py
	"""
	publico = Entidad.objects.get(schema_name='public')
	connection.set_tenant(publico)
	for d in deportes:
		try:
			mod = modalidades[d]
		except:
			mod = []
		for m in mod:
			ModalidadDisciplinaDeportiva(nombre=m['nombre'],descripcion=m['descripcion'],general=m['general']).save()

		try:
			cat = categorias[d]
		except:
			cat = []
		for c in cat:
			CategoriaDisciplinaDeportiva(nombre=c['nombre'],descripcion=c['descripcion'],general=c['general']).save()
#insertar_actualizar_deportes()