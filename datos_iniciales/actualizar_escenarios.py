from django.db import connection
from snd.modelos.escenarios import *
from entidades.models import *


entidades = Entidad.objects.exclude(schema_name="public")
for entidad in entidades:
    connection.set_tenant(entidad)
    mantenimientos = Mantenimiento.objects.all()
    if mantenimientos.count() == 0:
        continue
    else:
        for mantenimiento in mantenimientos:
            escenario_id = mantenimiento.escenario_id
            tiene_planos = mantenimiento.tiene_planos
            print(escenario_id,tiene_planos)
            caracterizacion = CaracterizacionEscenario.objects.get(escenario_id=escenario_id)
            caracterizacion.tiene_planos = tiene_planos
            caracterizacion.save()