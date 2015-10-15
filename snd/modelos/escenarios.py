#encoding:utf-8

from entidades.models import *
from django.db import models

class Escenario(models.Model):
    estratos = (
        ('1', 'Uno'),
        ('2', 'Dos'),
        ('3', 'Tres'),
        ('4', 'Cuatro'),
        ('5', 'Cinco'),
        ('6', 'Seis'),
    )
    ESTADOS = (
        (0,'ACTIVO'),
        (1,'INACTIVO'),
        (2,'EN TRANSFERENCIA'),
        (3,'TRANSFERIDO'),
    )
    DIVISIONES = (
        ('CP','Centro Poblado'),
        ('ZR','Zona Rural'),
        ('ZU','Zona Urbana'),
    )
    nombre =  models.CharField(max_length=100,unique=True)
    direccion = models.CharField(max_length=100)
    latitud = models.FloatField(null=True, blank=True)
    longitud = models.FloatField(null=True, blank=True)
    altura = models.PositiveIntegerField(null=True, blank=True)
    nombre_administrador = models.CharField(max_length=50, null=True)
    comuna = models.PositiveIntegerField()
    barrio = models.CharField(max_length=20)
    nombre_administrador = models.CharField(max_length=50, null=True)
    estrato = models.CharField(choices=estratos, max_length=1)
    entidad = models.ForeignKey(Entidad)    
    estado = models.IntegerField(choices=ESTADOS, verbose_name="estado del Escenario")
    ciudad = models.ForeignKey(Ciudad)
    division_territorial = models.CharField(choices=DIVISIONES, max_length=2, verbose_name="división territorial")    
    descripcion = models.CharField(max_length=1024, verbose_name='descripción', null=True)

    def fotos(self):
        return [x.foto for x in Foto.objects.filter(escenario=self)]

    def caracteristicas(self):
        return CaracterizacionEscenario.objects.get(escenario=self)

    def capacidad(self):
        return self.caracteristicas().capacidad_espectadores

    def tipo_escenario(self):
        return self.caracteristicas().tipo_escenario

    def obtenerAtributos(self):
        from django.conf import settings
        imagen = None
        fotos = Foto.objects.filter(escenario=self)
        if len(fotos) > 0:
            imagen = ("%s%s")%(settings.MEDIA_URL, fotos[0].foto.__str__())
        else:
            imagen = ("%s%s")%(settings.STATIC_URL, "img/actores/EscenarioView.PNG")

        atributos = [
            ["Nombre", self.nombre],
            ["Ciudad", self.ciudad.nombre],
            ["Comuna", self.comuna],
            ["Barrio", self.barrio],
            ["Estrato", self.estrato],
            ["Dirección", self.direccion],
            ["Latitud", self.latitud],
            ["Longitud", self.longitud],
        ]

        return [imagen, atributos, self.latitud, self.longitud, "Escenario!"]

class CaracterizacionEscenario(models.Model):   
    ACCESOS = (
        ('pr', 'Privado'),
        ('dul', 'De Uso Libre'),
        ('pcp', 'Público Con Pago'),
    )
    ESTADOS_FISICOS = (
        ('bu', 'Bueno'),
        ('re', 'Regular'),
        ('ma', 'Malo'),
    )
    PROPIETARIOS = (
        ('of', 'Oficial'),
        ('pr', 'Privado'),
    )
    escenario = models.ForeignKey(Escenario)
    metros_construidos = models.CharField(max_length=50, verbose_name='metros cuadrados construídos')
    caracteristicas = models.ManyToManyField(CaracteristicaEscenario)
    tipo_escenario = models.ForeignKey(TipoEscenario)
    tipo_superficie_juego = models.ManyToManyField(TipoSuperficie)
    clase_acceso = models.CharField(choices=ACCESOS, max_length=3, verbose_name='tipo de acceso') 
    tipo_disciplinas = models.ManyToManyField(TipoDisciplinaDeportiva)
    estado_fisico = models.CharField(choices=ESTADOS_FISICOS, max_length=2)
    capacidad_espectadores = models.CharField(max_length=50, verbose_name='capacidad de zona espectadores')
    espectadores_habituales = models.PositiveIntegerField(verbose_name='cantidad de espectadores habituales')
    clase_uso = models.ManyToManyField(TipoUsoEscenario)
    tipo_propietario = models.CharField(max_length=2, verbose_name='tipo de propietario', choices=PROPIETARIOS)
    ligas = models.ManyToManyField(Liga)
    descripcion = models.CharField(max_length=1024, verbose_name='descripción', null=True)

class HorarioDisponibilidad(models.Model):
    escenario = models.ForeignKey(Escenario)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    dias = models.ManyToManyField(Dias)
    descripcion = models.CharField(max_length=1024)

def ruta_fotos_escenarios(instance, filename):
    return "snd/fotos/escenarios/%s"%(filename.encode('ascii','ignore').decode('ascii'))

class Foto(models.Model):
    escenario = models.ForeignKey(Escenario)
    titulo = models.CharField(max_length=255, verbose_name="título")
    foto = models.ImageField(upload_to=ruta_fotos_escenarios, null=True, blank=True)
    descripcion = models.TextField(blank=True, null=True, max_length=1024)


class Video(models.Model):
    escenario = models.ForeignKey(Escenario)
    url = models.CharField(max_length=1024, verbose_name='url', null=True)
    descripcion = models.CharField(max_length=1024, null=True)

class Mantenimiento(models.Model):

    PERIODICIDADES = (
        ('di', 'Diaria'),
        ('se', 'Semanal'),
        ('qu', 'Quincenal'),
        ('me', 'Mensual'),
        ('bm', 'Bimestral'),
        ('tm', 'Trimestral'),
        ('sm', 'Semestral'),
        ('an', 'Anual'),
    )
    escenario = models.ForeignKey(Escenario)
    fecha_ultimo_mantenimiento = models.DateField( verbose_name="fecha del último mantenimiento", null=True, blank=True)
    descripcion_ultimo_mantenimiento = models.TextField(null=True, blank=True, max_length=1024, verbose_name='descripción del último mantenimiento')
    periodicidad = models.CharField(choices=PERIODICIDADES, max_length=2, null=True, blank=True)    
    razones_no_mantenimiento = models.TextField(null=True, blank=True, max_length=1024, verbose_name="Si no se realiza mantenimiento, mencione las razones")

class DatoHistorico(models.Model):
    escenario = models.ForeignKey(Escenario)
    fecha_inicio = models.DateField()
    duracion = models.PositiveIntegerField(verbose_name="duración en días")
    descripcion = models.CharField(max_length=1024)

class Contacto(models.Model):
    escenario = models.ForeignKey(Escenario)
    nombre =  models.CharField(max_length=50)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    descripcion = models.CharField(max_length=1024, null=True)
