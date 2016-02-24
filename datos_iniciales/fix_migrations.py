from entidades.models import Entidad
from django.db import connection
from django.contrib.contenttypes.models import ContentType
entidades = Entidad.objects.exclude(schema_name='public')
for entidad in entidades:
    connection.set_tenant(entidad)
    try:
        ct = ContentType.objects.filter(model__endswith='view').filter(model__startswith='public')
        ct.delete()
    except Exception:
        pass
    try:
        ct = ContentType.objects.filter(model__endswith='view').filter(model__startswith='tenant')
        ct.delete()
    except Exception:
        pass
    try:
        ct = ContentType.objects.get(model='reporteescenarioview')
        ct.delete()
    except Exception:
        pass