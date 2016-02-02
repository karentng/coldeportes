from django.db import connection
from entidades.models import Entidad,Federacion,ModalidadDisciplinaDeportiva,Liga,Club,EscuelaDeportiva_,TipoDisciplinaDeportiva
from snd.modelos.deportistas import Deportista
from snd.modelos.escenarios import CaracterizacionEscenario


entidades = Entidad.objects.exclude(schema_name='public')
#DISCIPLINA A BORRAR TRIATHLON
triathlon = TipoDisciplinaDeportiva.objects.get(id=82)
#DISCIPLINA CORRECTA
triatlon = TipoDisciplinaDeportiva.objects.get(id=42)

#ACTIVIDADES SUBACUATICO QUE SE DEBE BORRAR
subacuaticas1 = TipoDisciplinaDeportiva.objects.get(id=55)
print(subacuaticas1)
#ACTIVIDADES SUBACUATICAS CORRECTO
subacuaticas2 = TipoDisciplinaDeportiva.objects.get(id=23)

for entidad in entidades:
    connection.set_tenant(entidad)
    #TRIATLONES
    federaciones = Federacion.objects.filter(disciplina=triathlon).update(disciplina=triatlon)
    modalidades = ModalidadDisciplinaDeportiva.objects.filter(tipo=triathlon).update(tipo=triatlon)
    ligas = Liga.objects.filter(disciplina=triathlon).update(disciplina=triatlon)
    clubes = Club.objects.filter(disciplina=triathlon).update(disciplina=triatlon)
    escuelas = EscuelaDeportiva_.objects.filter(disciplina=triathlon)
    for escuela in escuelas:
        escuela.disciplina.remove(triathlon)
        escuela.disciplina.add(triatlon)
    deportistas = Deportista.objects.filter(disciplinas=triathlon)
    for deportista in deportistas:
        deportista.disciplinas.remove(triathlon)
        deportista.disciplinas.add(triatlon)
    caracterizaciones = CaracterizacionEscenario.objects.filter(tipo_disciplinas=triathlon)
    for caracterizacion in caracterizaciones:
        caracterizacion.tipo_disciplinas.remove(triathlon)
        caracterizacion.tipo_disciplinas.add(triatlon)
    #SUBACUATICAS
    federaciones = Federacion.objects.filter(disciplina=subacuaticas1).update(disciplina=subacuaticas2)
    modalidades = ModalidadDisciplinaDeportiva.objects.filter(tipo=subacuaticas1).update(tipo=subacuaticas2)
    ligas = Liga.objects.filter(disciplina=subacuaticas1).update(disciplina=subacuaticas2)
    clubes = Club.objects.filter(disciplina=subacuaticas1).update(disciplina=subacuaticas2)
    escuelas = EscuelaDeportiva_.objects.filter(disciplina=subacuaticas1)
    for escuela in escuelas:
        escuela.disciplina.remove(subacuaticas1)
        escuela.disciplina.add(subacuaticas2)
    deportistas = Deportista.objects.filter(disciplinas=subacuaticas1)
    for deportista in deportistas:
        deportista.disciplinas.remove(subacuaticas1)
        deportista.disciplinas.add(subacuaticas2)
    caracterizaciones = CaracterizacionEscenario.objects.filter(tipo_disciplinas=subacuaticas1)
    for caracterizacion in caracterizaciones:
        caracterizacion.tipo_disciplinas.remove(subacuaticas1)
        caracterizacion.tipo_disciplinas.add(subacuaticas2)