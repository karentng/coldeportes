from django.db import models
from tenant_schemas.models import TenantMixin

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

#General para deportistas y escenarios
class TipoDisciplinaDeportiva(models.Model):
    descripcion = models.CharField(max_length=50, verbose_name='descripción')

    def __str__(self):
        return self.descripcion

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
        (1, 'Liga'),
        (2, 'Federación'),
        (3, 'Club'),
        (4, 'Cajas de Compensación'),
        (5, 'Ente'),
        (6, 'Comité'),
        (7,'Federación Paralimpica'),
    )
    nombre = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255, verbose_name="dirección")
    pagina_web = models.URLField(verbose_name="página web propia", blank=True, null=True)
    telefono = models.CharField(max_length=255, verbose_name="teléfono", blank=True)
    descripcion = models.TextField(verbose_name="descripción", blank=True, null=True)

    tipo = models.IntegerField(choices=TIPOS)
    actores = models.OneToOneField(Actores, null=True)
    auto_create_schema = True

    def obtenerTenant(self):
        if self.tipo == 1:
            modelo = Liga
        elif self.tipo == 2:
            modelo = Federacion
        elif self.tipo == 3:
            modelo = Club
        elif self.tipo == 4:
            modelo = CajaDeCompensacion
        elif self.tipo == 5:
            modelo = Ente
        elif self.tipo == 6:
            modelo = Comite
        elif self.tipo == 7:
            modelo= FederacionParalimpica
        
        return modelo.objects.get(id=self.id)

    def __str__(self):
        return self.nombre

class Ente(Entidad):
    TIPOS_ENTE = (
        (1, 'Ente Municipal'),
        (2, 'Ente Departamental'),
    )
    ciudad = models.ForeignKey(Ciudad)
    tipo_ente = models.IntegerField(choices=TIPOS_ENTE)

class Comite(Entidad):
    TIPOS_COMITE = (
        (1, 'Comité Olimpico Colombiano'),
        (2, 'Comité Paralímpico Colombiano'),
    )
    ciudad = models.ForeignKey(Ciudad)
    tipo_comite = models.IntegerField(choices=TIPOS_COMITE)

class FederacionParalimpica(Entidad):
    discapacidad = models.CharField(max_length=100)
    comite = models.ForeignKey(Comite)

class CajaDeCompensacion(Entidad):
    ciudad = models.ForeignKey(Ciudad)

class Federacion(Entidad):
    disciplina = models.ForeignKey(TipoDisciplinaDeportiva)
    comite = models.ForeignKey(Comite)

class Liga(Entidad):
    federacion = models.ForeignKey(Federacion, null=True, blank=True, verbose_name="federación")
    departamento = models.ForeignKey(Departamento)
    disciplina = models.ForeignKey(TipoDisciplinaDeportiva)

class Club(Entidad):
    liga = models.ForeignKey(Liga, null=True, blank=True)
    ciudad = models.ForeignKey(Ciudad)

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
    descripcion = models.CharField(max_length=100, verbose_name='descripción')

    def __str__(self):
        return self.descripcion

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
