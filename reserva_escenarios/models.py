from django.db import models
from snd.modelos.escenarios import Escenario

# Create your models here.

class ReservaEscenario(models.Model):
    escenario = models.ForeignKey(Escenario)
    fecha_inicio = models.DateTimeField(null=True)
    fecha_fin = models.DateTimeField(null=True)
    decripcion = models.TextField(max_length = 500, verbose_name = 'descripción')
    nombre_equipo = models.CharField(max_length = 150,verbose_name = 'nombre de grupo que utilizará el escenario') 
    nombre_solicitante = models.CharField(max_length = 150,verbose_name = 'nombre') 
    identificacion_solicitante = models.CharField(max_length = 150,verbose_name = 'número de identificación')
    telefono_solicitante = models.CharField(max_length = 150,verbose_name = 'teléfono')
    direccion_solicitante = models.CharField(max_length = 150,verbose_name = 'dirección')
    aprobada = models.BooleanField(default = False)
