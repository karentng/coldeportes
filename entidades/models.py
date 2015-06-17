from django.db import models
from tenant_schemas.models import TenantMixin

class Entidad(TenantMixin): # Entidad deportiva
	nombre = models.CharField(max_length=255)
	auto_create_schema = True


class Departamento(models.Model):
	nombre = models.CharField(max_length=255, verbose_name='nombre')
	codigo = models.CharField(max_length=10, null=True, verbose_name='código')
	latitud = models.FloatField(null=True)
	longitud = models.FloatField(null=True)

	def __str__(self):
		return self.nombre

class Ciudad(models.Model):
	nombre = models.CharField(max_length=255, verbose_name='nombre')
	departamento = models.ForeignKey(Departamento)
	codigo = models.CharField(max_length=10, null=True, verbose_name='código')
	latitud = models.FloatField(null=True)
	longitud = models.FloatField(null=True)

	def __str__(self):
		return ("%s (%s)")%(self.nombre, self.departamento.nombre)

class Nacionalidad(models.Model):
	iso = models.CharField(max_length=5,verbose_name='Abreviacion')
	nombre = models.CharField(max_length=255,verbose_name='pais')

	def __str__(self):
		return self.nombre

class Dias(models.Model):
	nombre = models.CharField(max_length=10)

	def __str__(self):
		return self.nombre

class TipoEscenario(models.Model):
	descripcion = models.CharField(max_length=50, verbose_name='descripción')

	def __str__(self):
		return self.descripcion

class TipoDisciplinaEscenario(models.Model):
	descripcion = models.CharField(max_length=50, verbose_name='descripción')

	def __str__(self):
		return self.descripcion

#General para deportistas y escenarios
class TipoDisciplinaDeportiva(models.Model):
	descripcion = models.CharField(max_length=50, verbose_name='descripción')

	def __str__(self):
		return self.descripcion

class TipoUsoEscenario(models.Model):
	descripcion = models.CharField(max_length=50, verbose_name='descripción')

	def __str__(self):
		return self.descripcion

class CaracteristicaEscenario(models.Model):
	descripcion = models.CharField(max_length=50, verbose_name='descripción')

	def __str__(self):
		return self.descripcion
		return self.nombre
