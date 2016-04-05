#encoding:utf-8
from django.db import models
from snd.models import Escenario
from entidades.models import Entidad
import os
# Create your models here.
class SolicitudEscenario(models.Model):
    TIPOS= (
        (0,'ADECUACIÓN'),
        (1,'DOTACIÓN'),
        (2,'CONSTRUCCIÓN'),
    )
    PRIORIDADES = (
        (0,'BAJA'),
        (1,'MEDIA'),
        (2,'ALTA'),
    )
    ESTADOS = (
        (0,'ESPERANDO RESPUESTA'),
        (1,'INCOMPLETA'),
        (2,'APROBADA'),
        (3,'ANULADA'),
        (4,'CANCELADA POR ENTIDAD'),
    )

    VINCULOS = (
        (0,'USUARIO EXTERNO'),
        (1,'CONTRATISTA'),
        (2,'FUNCIONARIO'),
    )

    ESTADOS_ESCENARIO = (
        ('BUENO','BUENO'),
        ('REGULAR','REGULAR'),
        ('MALO','MALO'),
    )

    escenarios = models.ManyToManyField(Escenario)
    tipo = models.IntegerField(choices=TIPOS,verbose_name='Tipo de solicitud')
    prioridad = models.IntegerField(choices=PRIORIDADES)
    estado = models.IntegerField(choices=ESTADOS,default=0)
    descripcion = models.TextField(verbose_name='Descripción')
    para_quien = models.ForeignKey(Entidad,verbose_name='Dirigido a')
    estado_actual_escenario = models.CharField(max_length=50,choices=ESTADOS_ESCENARIO)
    nombre_solicitante = models.CharField(max_length=150,verbose_name='Nombre')
    id_solicitante = models.CharField(max_length=150,verbose_name='Número de identificación')
    tel_solicitante = models.CharField(max_length=150,verbose_name='Teléfono')
    direccion_solicitante = models.CharField(max_length=150,verbose_name='Dirección')
    vinculo_solicitante = models.IntegerField(choices=VINCULOS,verbose_name='Vinculo con la entidad')

    fecha = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = (
            ("view_solicitudescenario", "Permite ver solicitudes"),
        )

    def codigo_unico(self,entidad):
        return ("AD-%s-%s-%s")%(entidad.id,self.para_quien.id,self.id)

    def adjuntos(self):
        return AdjuntoSolicitud.objects.filter(solicitud=self)

    def escenarios_str(self):
        return ','.join([e.nombre for e in self.escenarios.all()])

    def save(self, *args, **kwargs):
        self.descripcion = self.descripcion.upper()
        self.estado_actual_escenario = self.estado_actual_escenario.upper()
        self.nombre_solicitante = self.nombre_solicitante.upper()
        self.id_solicitante = self.id_solicitante.upper()
        self.direccion_solicitante = self.direccion_solicitante.upper()
        super(SolicitudEscenario, self).save(*args, **kwargs)

class DiscucionSolicitud(models.Model):
    ESTADOS = (
        (0,'ESPERANDO RESPUESTA'),
        (1,'INCOMPLETA'),
        (2,'APROBADA'),
        (3,'RECHAZADA'),
    )

    estado_anterior = models.IntegerField(choices=ESTADOS)
    estado_actual = models.IntegerField(choices=ESTADOS, verbose_name='Cambiar estado a')
    descripcion = models.TextField(verbose_name="Descripción")
    solicitud = models.ForeignKey(SolicitudEscenario)
    fecha = models.DateTimeField(auto_now=True)
    entidad = models.ForeignKey(Entidad)
    respuesta = models.BooleanField()

    def tiene_adjuntos(self):
        if AdjuntoSolicitud.objects.filter(discucion=self):
            return True
        return False

class AdjuntoSolicitud(models.Model):
    solicitud = models.ForeignKey(SolicitudEscenario)
    archivo = models.FileField(upload_to="adjuntos_adecuacion_escenarios",verbose_name='Archivo a adjuntar')
    discucion = models.ForeignKey(DiscucionSolicitud,null=True,blank=True)

    def __str__(self):
        return self.nombre_archivo()

    def nombre_archivo(self):
        return os.path.basename(self.archivo.name)

    def icon_extension(self):
        name, extension = os.path.splitext(self.archivo.name)
        if extension in ['.pdf','.PDF']:
            return 'pdf'
        if extension in ['.doc','.docx', '.DOC','.DOCX']:
            return 'word'
        if extension in ['.xls','.xlsx','.XLS','.XLSX']:
            return 'excel'
        if extension in ['.zip','.rar','.ZIP','.RAR']:
            return 'zip'
        if extension in ['.jpg','.jpeg','.png','.gif','.JPG','.JPEG','.PNG','.GIF']:
            return 'picture'
        if extension in ['.ppt','.pptx','.PPT','.PPTX']:
            return 'powerpoint'
        return 'file'

    def save(self, *args, **kwargs):
        name, extension = os.path.splitext(self.archivo.name)
        next_id = AdjuntoSolicitud.objects.filter(solicitud=self.solicitud).count() + 1
        self.archivo.name = "AdjuntoSolicitud"+str(next_id)+str(self.solicitud.id)+extension
        super(AdjuntoSolicitud, self).save(*args, **kwargs)
