from entidades.models import Entidad, ModalidadDisciplinaDeportiva, TipoDisciplinaDeportiva,CategoriaDisciplinaDeportiva
from datos_iniciales.disciplinas_deportivas.modalidades_categorias import *
from django.db import connection

deportes = [
    'Parapentismo', 'Aeromodelismo', 'Ala delta ', 'Ultralivianos', 'Planeadores', 'Globos aerostáticos', 'Apnea',
    'Natación con aletas', 'Buceo', 'Hockey subacuático', 'Rugby subacuático', 'Pesca submarina', 'Orientación',
    'Automovilismo deportivo', '(Automovilismo deportivo) - Rallies colombiano','(Automovilismo deportivo) - Rallie Cross',
    '(Automovilismo deportivo) - Camper Cross', '(Automovilismo deportivo) - Velocidad', 'Ajedrez', 'Arquería', 'Bolos',
    'Ecuestre', 'Esgrima', 'Esquí Náutico', 'Futbol de salón', 'Golf', 'Hapkido', 'Karts', 'Motociclismo','Motonáutica Squash',
    'Softbol', 'Tenis de mesa', 'Voleibol', 'Deportes Fuerzas Armadas', 'Deporte montaña y escalada','Coleo', 'Billar',
    'Nado sincronizado', 'Waterpolo', 'Bádminton', 'Baloncesto', 'Canotaje', 'Balonmano', 'Hockey', 'Pentatlón moderno',
    'Vela', 'Tejo','Tiro y caza', 'Trampolín', 'Triatlón'
]

def insertar_actualizar_deportes():
    """
    Enero 30,2016
    Autor: Daniel Correa

    Permite actualizar o crear los registros de tipo disciplina deportiva sin dañar los registros existentes
    """
    publico = Entidad.objects.get(schema_name='public')
    connection.set_tenant(publico)
    all_dis = TipoDisciplinaDeportiva.objects.all()
    last_id = all_dis[len(all_dis)-1].id
    for d in deportes:
        try:
            TipoDisciplinaDeportiva.objects.get(descripcion=d)
        except Exception:
            dep = TipoDisciplinaDeportiva(descripcion=d,id=last_id)
            dep.save()
            last_id+=1
    asa = TipoDisciplinaDeportiva.objects.get(descripcion='Actividades Subacuaticas')
    asa.descripcion = 'Actividades Subacuáticas'
    asa.save()


def insertar_modalidades_categorias():
    """
    Enero 30, 2016
    Autor: Daniel Correa

    Permite insertar las modalidades y categorias de los JSON que estan en el archivo modalidades_categorias.py
    """
    publico = Entidad.objects.get(schema_name='public')
    connection.set_tenant(publico)
    for d in deportes:
        depor = TipoDisciplinaDeportiva.objects.get(descripcion=d)
        try:
            mod = modalidades[d]
        except:
            mod = []
        for m in mod:
            ModalidadDisciplinaDeportiva(nombre=m['nombre'], descripcion=m['descripcion'], general=m['general'],deporte=depor).save()
        try:
            cat = categorias[d]
        except:
            cat = []
        for c in cat:
            CategoriaDisciplinaDeportiva(nombre=c['nombre'], descripcion=c['descripcion'], general=c['general'],deporte=depor).save()