from django.db import models
from entidades.models import Entidad
# Create your models here.
class ListaSolicitudes(models.Model):
    entidad_solicitante = models.ForeignKey(Entidad)
    solicitud = models.PositiveIntegerField()
