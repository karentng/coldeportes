from django.db import models
from entidades.models import Entidad, Ciudad

class ReporteCafView(models.Model):
	class Meta:
		managed = False

	ciudad = models.ForeignKey(Ciudad)
	comuna = models.PositiveIntegerField()
	estrato = models.PositiveIntegerField()
	latitud = models.FloatField()
	longitud = models.FloatField()
	altura = models.PositiveIntegerField()
	estado = models.IntegerField()
	entidad = models.ForeignKey(Entidad)
	fecha_creacion = models.DateTimeField()
	nombre_clase = models.CharField(max_length=255)
	nombre_servicio = models.CharField(max_length=255)