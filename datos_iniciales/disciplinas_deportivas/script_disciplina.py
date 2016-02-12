from entidades.models import Entidad, ModalidadDisciplinaDeportiva, TipoDisciplinaDeportiva,CategoriaDisciplinaDeportiva
from datos_iniciales.disciplinas_deportivas.modalidades_categorias import *
from django.db import connection

deportes = [
    'Parapentismo', 'Aeromodelismo', 'Ala delta', 'Ultralivianos', 'Planeadores', 'Globos aerostáticos', 'Apnea',
    'Natación con aletas', 'Buceo', 'Hockey subacuático', 'Rugby subacuático', 'Pesca submarina', 'Orientacion',
    'Automovilismo deportivo','(Automovilismo deportivo) - Rallies colombiano','(Automovilismo deportivo) - Rallie Cross',
    '(Automovilismo deportivo) - Camper Cross', '(Automovilismo deportivo) - Velocidad', 'Ajedrez', 'Arquería', 'Bolos',
    'Ecuestre', 'Esgrima', 'Esquí Náutico', 'Futbol De Salon', 'Golf', 'Hapkido', 'Karts', 'Motociclismo','Motonautica', 'Squash',
    'Softbol', 'Tenis de mesa', 'Voleibol', 'Deportes Fuerzas Armadas', 'Deporte montaña y escalada','Coleo', 'Billar',
    'Nado sincronizado', 'Waterpolo', 'Badminton', 'Baloncesto', 'Canotaje', 'Balonmano', 'Hockey', 'Pentatlón moderno',
    'Vela', 'Tejo','Tiro Y Caza', 'Trampolín', 'Triatlón','Boccia', 'Baloncesto en Silla de Ruedas', 'Ciclismo Tandem',
    'Slalom', 'Tenis De Campo en Silla de Ruedas', 'Goalball', 'Powerlifting', 'Paracycling', 'Tenis en Silla de Ruedas',
    'Ciclismo','Ciclismo BMX','Ciclismo de montaña','Ciclismo en pista','Ciclismo en ruta','Fútbol','Natación','Tenis','Rugby'
]

def insertar_actualizar_deportes():
    """
    Enero 30,2016
    Autor: Daniel Correa

    Permite actualizar o crear los registros de tipo disciplina deportiva sin dañar los registros existentes
    """
    publico = Entidad.objects.get(schema_name='public')
    connection.set_tenant(publico)
    all_dis = TipoDisciplinaDeportiva.objects.all().order_by('id')
    last_id = all_dis[len(all_dis)-1].id + 1

    autom = TipoDisciplinaDeportiva.objects.get(descripcion='Automovilismo')
    autom.descripcion = 'Automovilismo deportivo'
    autom.save()

    for d in deportes:
        try:
            TipoDisciplinaDeportiva.objects.get(descripcion=d)
        except Exception as e:
            print(d)
            dep = TipoDisciplinaDeportiva(descripcion=d,id=last_id)
            dep.save()
            last_id+=1
    asa = TipoDisciplinaDeportiva.objects.get(descripcion='Actividades Subacuaticas')
    asa.descripcion = 'Actividades Subacuáticas'
    asa.save()
    
    print('Deportes actualizados correctamente')


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
    print('Modalidades y categorias insertadas exitosamente')