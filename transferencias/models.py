from django.db import models
from entidades.models import Entidad
# Create your models here.
class Transferencia(models.Model):
    TIPOS_ESTADO_TANSFERENCIA = (
        ('Pendiente','Pendiente'),
        ('Aprobada','Aprobada'),
        ('Rechazada','Rechazada'),
    )
    fecha_solicitud = models.DateField()
    tipo_objeto = models.CharField(max_length=100)
    id_objeto = models.IntegerField()
    estado = models.CharField(choices=TIPOS_ESTADO_TANSFERENCIA,default='Pendiente',max_length=20)
    entidad = models.ForeignKey(Entidad)

    def __str__(self):
        return str(self.fecha_solicitud)+':'+str(self.tipo_objeto)