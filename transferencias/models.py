from django.db import models
from entidades.models import Entidad
# Create your models here.
class Transferencia(models.Model):
    fecha_solicitud = models.DateField()
    tipo_objeto = models.CharField(max_length=100)
    id_objeto = models.IntegerField()
    entidad = models.ForeignKey(Entidad)