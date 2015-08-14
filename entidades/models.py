from django.db import models
from tenant_schemas.models import TenantMixin

class Actores(models.Model):
    centros = models.BooleanField(verbose_name="Centros de Acondicionamiento Físico")
    escenarios = models.BooleanField(verbose_name="Escenarios")
    deportistas = models.BooleanField(verbose_name="Deportistas")
    personal_apoyo = models.BooleanField(verbose_name="Personal de apoyo")
    dirigentes = models.BooleanField(verbose_name="Dirigentes")
    cajas = models.BooleanField(verbose_name="Cajas de Compensación")

    def resumen(self):
        actores = []
        campos = self._meta.fields
        for i in campos:
            if getattr(self, i.name) == True and i.name != 'id':
                actores.append(i.verbose_name)
        return actores

class Entidad(TenantMixin): # Entidad deportiva
    TIPOS = (
        (1, 'Ente Municipal'),
        (2, 'Ente Departamental'),
        (3, 'Club'),
        (4, 'Cajas de Compensación'),
    )
    nombre = models.CharField(max_length=255)
    tipo = models.IntegerField(choices=TIPOS, null=True)
    actores = models.OneToOneField(Actores, null=True)
    auto_create_schema = True

    def __str__(self):
        return self.nombre

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

class TipoSuperficie(models.Model):
    disciplina = models.CharField(max_length=50, null=True)
    descripcion = models.CharField(max_length=100, verbose_name='descripción')

    def __str__(self):
        return self.disciplina+", "+self.descripcion

class TipoServicioCajaCompensacion(models.Model):
    categoria = models.CharField(max_length=50, verbose_name='categoría')
    descripcion = models.CharField(max_length=100, verbose_name='descripción')

    def __str__(self):
        return self.descripcion

class TipoServicioEscenarioCajaCompensacion(models.Model):
    descripcion = models.CharField(max_length=100, verbose_name='descripción')

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

class CAClase(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class CAServicio(models.Model):
    nombre = models.CharField(max_length=255)
    
    def __str__(self):
        return self.nombre

class EPS(models.Model):
    nombre = models.CharField(max_length=300)
    codigo = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
