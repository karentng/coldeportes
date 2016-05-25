from django.db import models
from snd.modelos.escenarios import Escenario

# Create your models here.

class ReservaEscenario(models.Model):
    escenario = models.ForeignKey(Escenario)
    fecha_inicio = models.DateTimeField(null=True)
    fecha_fin = models.DateTimeField(null=True)
    nombre_equipo = models.CharField(max_length = 150,verbose_name = 'nombre del grupo que utilizará el escenario') 
    nombre_solicitante = models.CharField(max_length = 150,verbose_name = 'nombre del solicitante') 
    identificacion_solicitante = models.CharField(max_length = 150,verbose_name = 'número de identificación del solicitante')
    telefono_solicitante = models.CharField(max_length = 150,verbose_name = 'teléfono de contacto')
    direccion_solicitante = models.CharField(max_length = 150,verbose_name = 'dirección de contacto')
    descripcion = models.TextField(max_length = 500, verbose_name = 'descripción de la actividad')
    aprobada = models.BooleanField(default = False)


class ConfiguracionReservaEscenario(models.Model):
    escenario = models.OneToOneField(Escenario)
    cantidad_maxima_horas = models.PositiveIntegerField(verbose_name = "cantidad máxima de horas que se puede reservar el escenario")
    cantidad_minima_horas = models.PositiveIntegerField(default = 1, verbose_name = "cantidad mínima de horas que se puede reservar el escenario")


