from django.db import models
from snd.models import Escenario
from entidades.models import Entidad
# Create your models here.
class SolicitudEscenario(models.Model):
    TIPOS= ()
    PRIORIDADES = (
        (0,'BAJA'),
        (1,'MEDIA'),
        (2,'ALTA'),
    )
    ESTADOS = (
        (0,'ESPERANDO RESPUESTA'),
        (1,'INCOMPLETA'),
        (2,'APROBADA'),
        (3,'ANULADA')
    )

    escenarios = models.ManyToManyField(Escenario)
    tipo = models.IntegerField(choices=TIPOS)
    prioridad = models.IntegerField(choices=PRIORIDADES)
    descripcion = models.TextField()
    para_quien = models.ForeignKey(Entidad)

    def codigo_unico(self):
        return ("AD-%s-%s")%(self.para_quien.id,self.id)

class AdjuntoSolicitud(models.Model):
    solicitud = models.ForeignKey(SolicitudEscenario)
    archivo = models.FileField(upload_to="solicitudes_escenarios")

class DiscucionSolicitud(models.Model):
    ESTADOS = (
        (0,'ESPERANDO RESPUESTA'),
        (1,'INCOMPLETA'),
        (2,'APROBADA'),
        (3,'ANULADA')
    )

    estado_anterior = models.IntegerField(choices=ESTADOS)
    estado_actual = models.IntegerField(choices=ESTADOS)
    descripcion = models.TextField()
    solicitud = models.ForeignKey(SolicitudEscenario)

class ListaSolicitudes(models.Model):
    entidad_solicitante = models.ForeignKey(Entidad)
    solicitud = models.PositiveIntegerField()