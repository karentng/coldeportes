from django.db import connection
from entidades.models import Entidad,Federacion,ModalidadDisciplinaDeportiva,Liga,Club,EscuelaDeportiva,TipoDisciplinaDeportiva
from snd.modelos.deportistas import Deportista
from snd.modelos.escenarios import CaracterizacionEscenario



entidades = Entidad.objects.exclude(schema_name='public')
#DISCIPLINA A BORRAR TRIATHLON
triathlon = TipoDisciplinaDeportiva.objects.get(id=82)
#DISCIPLINA CORRECTA
triatlon = TipoDisciplinaDeportiva.objects.get(id=42)


for entidad in entidades:
    connection.set_tenant(entidad)
    federaciones = Federacion.objects.filter(disciplina__id=82).update(disciplina=42)