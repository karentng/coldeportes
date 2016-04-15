#encoding:utf-8
import os
from django.db import models
from django.db.models import Count
from snd.models import Escenario
from entidades.models import Entidad, TipoRequerimientoReconocimientoDeportivo

# Create your models here.
class ReconocimientoDeportivo(models.Model):
    
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

    TIPO_SOLICITUD = (
        (0,'PRIMERA VEZ'),
        (1,'RENOVACIÓN'),
    )

    
    estado = models.IntegerField(choices=ESTADOS,default=1)
    descripcion = models.TextField(verbose_name='Descripción')
    para_quien = models.ForeignKey(Entidad,verbose_name='Dirigido a')    
    nombre_solicitante = models.CharField(max_length=150,verbose_name='Nombre') 
    tipo = models.IntegerField(choices=TIPO_SOLICITUD, verbose_name='tipo de solicitud')
    id_solicitante = models.CharField(max_length=150,verbose_name='Número de identificación')
    tel_solicitante = models.CharField(max_length=150,verbose_name='Teléfono')
    direccion_solicitante = models.CharField(max_length=150,verbose_name='Dirección')
    vinculo_solicitante = models.IntegerField(choices=VINCULOS,verbose_name='Vínculo con la entidad')
    fecha_vigencia = models.DateField(verbose_name="fecha de vigencia", null=True)
    fecha_creacion = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = (
            ("view_reconocimientodeportivo", "Permite ver solicitudes de reconocimiento deportivo"),
        )

    def codigo_unico(self,entidad):
        return ("RD-%s-%s-%s")%(entidad.id,self.para_quien.id,self.id)

    def adjuntos(self):
        return AdjuntoReconocimiento.objects.filter(solicitud=self)

    def cantidad_adjuntos(self):        
        return len(AdjuntoReconocimiento.objects.filter(solicitud=self, discusion=None))

    def save(self, *args, **kwargs):
        self.descripcion = self.descripcion.upper()
        self.nombre_solicitante = self.nombre_solicitante.upper()
        self.id_solicitante = self.id_solicitante.upper()
        self.direccion_solicitante = self.direccion_solicitante.upper()
        super(ReconocimientoDeportivo, self).save(*args, **kwargs)


class DiscusionReconocimiento(models.Model):
    ESTADOS = (
        (0,'ESPERANDO RESPUESTA'),
        (1,'INCOMPLETA'),
        (2,'APROBADA'),
        (3,'RECHAZADA'),
        (4,'EN DISCUSION'),
    )

    estado_anterior = models.IntegerField(choices=ESTADOS)
    estado_actual = models.IntegerField(choices=ESTADOS, verbose_name='Cambiar estado a')
    descripcion = models.TextField(verbose_name="Descripción")
    solicitud = models.ForeignKey(ReconocimientoDeportivo)
    fecha = models.DateTimeField(auto_now=True)
    entidad = models.ForeignKey(Entidad)
    respuesta = models.BooleanField()

    def tiene_adjunto(self):
        adjunto = AdjuntoReconocimiento.objects.get(discusion=self)
        return adjunto


class AdjuntoReconocimiento(models.Model):
    
    solicitud = models.ForeignKey(ReconocimientoDeportivo)
    discusion = models.ForeignKey(DiscusionReconocimiento,null=True,blank=True) 
    archivo = models.FileField(upload_to="adjuntos_reconocimiento_deportivo", null=True) 
    tipo = models.ForeignKey(TipoRequerimientoReconocimientoDeportivo)   

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
        next_id = AdjuntoReconocimiento.objects.filter(solicitud=self.solicitud).count() + 1
        self.archivo.name = "AdjuntoReconocimiento"+str(next_id)+str(self.solicitud.id)+extension
        super(AdjuntoReconocimiento, self).save(*args, **kwargs)
