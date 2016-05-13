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
