from django.db import models
from entidades.models import *


class TenantEscenarioView(models.Model):
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

    class Meta:
        managed = False
    #campos modelo escenario
    nombre =  models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    latitud = models.FloatField(max_length=10)
    longitud = models.FloatField(max_length=10)
    altura = models.PositiveIntegerField()
    ciudad = models.ForeignKey(Ciudad)
    comuna = models.PositiveIntegerField()
    barrio = models.CharField(max_length=20)
    estrato = models.CharField(max_length=1)
    nombre_administrador = models.CharField(max_length=50, null=True)
    entidad = models.ForeignKey(Entidad)    
    estado = models.IntegerField()
    #campos modelo caracterizacion
    tipo_escenario = models.ForeignKey(TipoEscenario)
    tipodisciplinadeportiva = models.ForeignKey(TipoDisciplinaDeportiva)
    estado_fisico = models.CharField(choices=ESTADOS_FISICOS, max_length=2)
    tiposuperficie = models.ForeignKey(TipoSuperficie)
    clase_acceso = models.CharField(max_length=3)

    #campos modelo contacto
    nombre_contacto =  models.CharField(max_length=50)
    telefono_contacto = models.CharField(max_length=20)
    email_contacto = models.EmailField()
    descripcion_contacto = models.CharField(max_length=1024, null=True)
    #campos modelo horario
    horario_id = models.IntegerField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    dias = models.ForeignKey(Dias)
    descripcion_horario = models.CharField(max_length=1024)
    #campos modelo Foto
    foto = models.ImageField(upload_to='fotos_escenarios', null=True, blank=True)

class TenantCafView(models.Model):
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

class TenantPersonalApoyoView(models.Model):
    class Meta:
        managed = False

    actividad = models.IntegerField()
    genero = models.CharField(max_length=11)
    tipo_id = models.CharField(max_length=5)
    fecha_nacimiento = models.DateField()
    nacionalidad = models.ManyToManyField(Nacionalidad)
    ciudad = models.ForeignKey(Ciudad)
    etnia = models.CharField(max_length=20)
    lgtbi = models.BooleanField()
    fecha_creacion = models.DateField()
    estado = models.IntegerField()
    nivel_formacion = models.CharField(max_length=20)
    estado_formacion = models.CharField(max_length=20)
    ano_final_formacion = models.IntegerField()
    creacion_formacion = models.DateField()