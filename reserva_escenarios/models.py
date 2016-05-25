from django.db import models
from snd.modelos.escenarios import Escenario

# Create your models here.

class ReservaEscenario(models.Model):  
    ESTADOS = (
        (1,'APROBADA'),
        (2,'ESPERANDO RESPUESTA'),
        (3,'RECHAZADA'),
    )  
    escenario = models.ForeignKey(Escenario)
    fecha_inicio = models.DateTimeField(null=True)
    fecha_fin = models.DateTimeField(null=True)
    nombre_equipo = models.CharField(max_length = 150,verbose_name = 'nombre del grupo que utilizará el escenario') 
    nombre_solicitante = models.CharField(max_length = 150,verbose_name = 'nombre del solicitante') 
    identificacion_solicitante = models.CharField(max_length = 150,verbose_name = 'número de identificación del solicitante')
    telefono_solicitante = models.CharField(max_length = 150,verbose_name = 'teléfono de contacto')
    direccion_solicitante = models.CharField(max_length = 150,verbose_name = 'dirección de contacto')
    correo_solicitante = models.EmailField(verbose_name = 'correo electrónico de contacto')
    descripcion = models.TextField(max_length = 500, verbose_name = 'descripción de la actividad')
    comentarios_respuesta = models.TextField(max_length = 500, verbose_name = 'comentarios')
    estado = models.IntegerField(choices=ESTADOS)
    fecha_creacion = models.DateField(auto_now_add=True)

    def codigo_unico(self, entidad):
        return ("RE-%s-%s-%s")%(entidad.id, self.escenario.id, self.id)

    def save(self, *args, **kwargs):
        self.nombre_equipo = self.nombre_equipo.upper()
        self.nombre_solicitante = self.nombre_solicitante.upper()
        self.direccion_solicitante = self.direccion_solicitante.upper()
        self.identificacion_solicitante = self.identificacion_solicitante.upper()
        self.descripcion = self.descripcion.upper()
        super(ReservaEscenario, self).save(*args, **kwargs)


class ConfiguracionReservaEscenario(models.Model):
    escenario = models.OneToOneField(Escenario)
    cantidad_maxima_horas = models.PositiveIntegerField(verbose_name = "cantidad máxima de horas que se puede reservar el escenario")
    cantidad_minima_horas = models.PositiveIntegerField(default = 1, verbose_name = "cantidad mínima de horas que se puede reservar el escenario")


