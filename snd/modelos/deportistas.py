#encoding:utf-8

from entidades.models import *
from django.db import models
from coldeportes.utilities import calculate_age,extraer_codigo_video
from django.db.models.fields.files import ImageFieldFile, FileField
from coldeportes.settings import STATIC_URL
from django.conf import settings
import os


class Deportista(models.Model):

    def foto_name(instance, filename):
        #el nombre de la imagen es la identificación del deportista, filename[-4:] indica la extensión del archivo
        #primero se borra alguna imagen existente que tenga el mismo nombre. Si la imagen anterior tiene una extensión distinta a la nueva se crea una copia
        ruta = 'fotos_deportistas/' + instance.identificacion + filename[-4:]
        ruta_delete = settings.MEDIA_ROOT + "/" + ruta
        if(os.path.exists(ruta_delete)):
            os.remove(ruta_delete)
        return ruta

    #Datos personales
        #Identificacion
    tipo_sexo = (
        ('HOMBRE','MASCULINO'),
        ('MUJER','FEMENINO'),
    )
    TIPO_IDENTIDAD = (
        ('CC', 'CÉDULA DE CIUDADANÍA'),
        ('TI', 'TARJETA DE IDENTIDAD'),
        ('CE', 'CÉDULA DE EXTRANJERÍA'),
        ('PS', 'PASAPORTE'),
    )
    ESTADOS = (
        (0,'ACTIVO'),
        (1,'INACTIVO'),
        (2,'EN TRANSFERENCIA'),
        (3,'TRANSFERIDO'),
    )

    ETNIAS = (
        ('MESTIZO','MESTIZO'),
        ('AFROCOLOMBIANO','AFROCOLOMBIANO'),
        ('BLANCO','BLANCO'),
        ('COLOMBOINDIGENA','COLOMBOINDIGENA'),
        ('GITANO','GITANO'),
        ('PALENQUERO','PALENQUERO'),
        ('RAIZAL','RAIZAL'),
    )

    nombres = models.CharField(max_length=100, verbose_name='Nombres')
    apellidos = models.CharField(max_length=100,verbose_name='Apellidos')
    genero = models.CharField(choices=tipo_sexo,max_length=11, verbose_name='Genero del Deportista')
    tipo_id = models.CharField(max_length=10, choices=TIPO_IDENTIDAD, default='CC',verbose_name='Tipo de Identificación')
    identificacion = models.CharField(max_length=100,verbose_name='Identificación')
    fecha_nacimiento = models.DateField(verbose_name='Fecha de nacimiento')
    ciudad_residencia = models.ForeignKey(Ciudad, verbose_name='Ciudad en donde esta residiendo')
    barrio = models.CharField(max_length=100,verbose_name='Barrio')
    comuna = models.CharField(max_length=100,verbose_name='Comuna')
    email = models.EmailField(null=True,blank=True)
    telefono = models.CharField(max_length=100,verbose_name='Teléfono')
    direccion = models.CharField(max_length=100,verbose_name='Dirección')
    lgtbi = models.BooleanField(verbose_name='Hace parte de la comunidad LGTBI?')
    entidad = models.ForeignKey(Entidad)

    estado = models.IntegerField(choices=ESTADOS, default=0, verbose_name="estado del Deportista")
    etnia = models.CharField(max_length=20, choices=ETNIAS,blank=True)

    video = models.URLField(max_length=1024, verbose_name='Video', null=True, blank=True)
    disciplinas = models.ManyToManyField(TipoDisciplinaDeportiva,verbose_name='Disciplinas Deportivas')
    nacionalidad = models.ManyToManyField(Nacionalidad,verbose_name='Nacionalidad')
    foto = models.ImageField(upload_to=foto_name, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('tipo_id','identificacion',)
        permissions = (
            ("view_deportista", "Permite ver deportista"),
        )

    def __str__(self):
        return self.identificacion + "-" + self.nombres+" "+self.apellidos

    def short_video_url(self):
        return extraer_codigo_video(self.video)

    def edad(self):
        return calculate_age(self.fecha_nacimiento)

    def disciplinas_deportivas(self):
        return ",".join(str(x) for x in self.disciplinas.all())

    def nacionalidad_str(self):
        return ",".join(x.nombre for x in self.nacionalidad.all())

    def fotos(self):
        return [self.foto]

    def full_name(self):
        return str(self.nombres) + " " +str(self.apellidos)

    def full_id(self):
        return str(self.get_tipo_id_display())+":"+str(self.identificacion)

    def save(self, *args, **kwargs):
        self.nombres = self.nombres.upper()
        self.apellidos = self.apellidos.upper()
        self.barrio = self.barrio.upper()
        self.comuna = self.comuna.upper()
        self.direccion = self.direccion.upper()
        super(Deportista, self).save(*args, **kwargs)


#Composicion corporal
class ComposicionCorporal(models.Model):
    tipos_rh =(
        ('A+','A+'),
        ('A-','A-'),
        ('B+','B+'),
        ('B-','B-'),
        ('AB+','AB+'),
        ('AB-','AB-'),
        ('O+','O+'),
        ('O-','O-'),
    )
    tipos_talla_choices = (
        ('Niño','Niño'),
        ('Adulto','Adulto'),
    )
    tallas_choices = (
        ('XS','XS'),
        ('S','S'),
        ('M','M'),
        ('L','L'),
        ('XL','XL'),
        ('XXL','XXL'),
    )
    deportista = models.ForeignKey(Deportista)
    peso = models.FloatField(help_text="En kg", verbose_name="Peso (kg)")
    estatura = models.IntegerField(help_text="En cm", verbose_name="Estatura (cm)")
    RH = models.CharField(max_length=4,choices=tipos_rh,verbose_name='Tipo de sangre')
    tipo_talla = models.CharField(max_length=7,choices=tipos_talla_choices,verbose_name='Talla para' )
    talla_camisa = models.CharField(max_length=3, choices=tallas_choices,verbose_name='Talla Camisa')
    talla_pantaloneta = models.CharField(max_length=3, choices=tallas_choices,verbose_name='Talla Pantaloneta')
    talla_zapato = models.CharField(max_length=2,verbose_name='Talla Zapato')
    imc = models.FloatField(verbose_name='Indice de Masa Corporal (kg/m^2)')
    porcentaje_grasa = models.FloatField(verbose_name='Porcentaje de Grasa Corporal (%)')
    masa_corporal_magra = models.FloatField(verbose_name='Masa Corporal Magra (kg)')
    eps = models.ForeignKey(EPS,verbose_name='EPS')
    fecha_inicia_deporte = models.DateField(verbose_name='Fecha de iniciación en el deporte')
    fecha_creacion = models.DateTimeField(auto_now_add=True)


#Hitorial deportivo
class HistorialDeportivo(models.Model):
    tipo_his_deportivo=(
        ('Campeonato Municipal','Campeonato Municipal'),
        ('Campeonato Departamental','Campeonato Departamental'),
        ('Campeonato Nacional','Campeonato Nacional'),
        ('Campeonato Internacional','Campeonato Internacional'),
    )

    ESTADOS_AVAL = (
        ('Aprobado','Aprobado'),
        ('Pendiente','Pendiente'),
        ('Rechazado','Rechazado'),
    )

    nombre = models.CharField(max_length=100,verbose_name='Nombre del campeonato')
    fecha_inicial = models.DateField(verbose_name='Fecha Iniciación')
    fecha_final = models.DateField(verbose_name='Fecha Finalización ')
    pais = models.ForeignKey(Nacionalidad)
    institucion_equipo = models.CharField(max_length=100, verbose_name='Club deportivo')
    tipo = models.CharField(choices=tipo_his_deportivo,max_length=100,verbose_name='Clase de campeonato')
    puesto = models.IntegerField(verbose_name='Puesto obtenido')
    marca = models.CharField(max_length=100,blank=True,verbose_name='Marca obtenida')
    modalidad = models.ForeignKey(ModalidadDisciplinaDeportiva,null=True,blank=True,verbose_name='Modalidad de competencia')
    division = models.CharField(max_length=100,blank=True,verbose_name='División de competencia')
    deporte = models.ForeignKey(TipoDisciplinaDeportiva,verbose_name='Deporte en el que participó')
    categoria = models.ForeignKey(CategoriaDisciplinaDeportiva,null=True,blank=True,verbose_name='Categoría en la que participó')
    estado = models.CharField(choices=ESTADOS_AVAL,default='Aprobado',max_length=50)
    deportista = models.ForeignKey(Deportista)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def obtener_info_aval(self):
        informacion = [
            self.deportista.foto,
            self.deportista.full_name(),
            self.deportista.entidad.nombre,
            self.deportista.full_id(),
            self.nombre,
            self.tipo,
            self.puesto,
            self.pais.nombre,
            self.institucion_equipo,
            self.id,
            self.deportista.entidad.id,
            self.fecha_inicial,
            self.fecha_final,
            self.categoria
        ]
        return informacion

    def __str__(self):
        return self.deportista.nombres+':'+self.nombre

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        self.marca = self.marca.upper()
        self.division = self.division.upper()
        self.institucion_equipo = self.institucion_equipo.upper()

        super(HistorialDeportivo, self).save(*args, **kwargs)

#Informacion academica
class InformacionAcademica(models.Model):
    tipo_academica = (
        ('Jardin','Jardin'),
        ('Primaria','Primaria'),
        ('Bachillerato','Bachillerato'),
        ('Técnico','Técnico'),
        ('Tecnólogo','Tecnólogo'),
        ('Pregrado','Pregrado'),
        ('Postgrado','Postgrado'),
    )
    tipo_estado = (
        ('Actual','Actual'),
        ('Finalizado','Finalizado'),
        ('Incompleto','Incompleto'),
    )
    pais = models.ForeignKey(Nacionalidad,verbose_name='País')
    institucion = models.CharField(max_length=100,verbose_name='Institución')
    nivel = models.CharField(choices=tipo_academica,max_length=20,verbose_name='Nivel')
    estado = models.CharField(choices=tipo_estado,max_length=20,verbose_name='Estado')
    profesion =  models.CharField(max_length=100,blank=True,null=True,verbose_name='Profesión')
    grado_semestre = models.IntegerField(verbose_name='Grado, Año o Semestre', null=True, blank=True)
    fecha_finalizacion = models.IntegerField(blank=True,null=True,verbose_name='Año Finalización')
    deportista = models.ForeignKey(Deportista)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.institucion = self.institucion.upper()
        self.profesion = self.profesion.upper()
        super(InformacionAcademica, self).save(*args, **kwargs)

class CambioDocumentoDeportista(models.Model):
    TIPO_IDENTIDAD = (
        ('TI', 'TARJETA DE IDENTIDAD'),
        ('CC', 'CÉDULA DE CIUDADANÍA'),
        ('CE', 'CÉDULA DE EXTRANJERÍA'),
        ('PS', 'PASAPORTE'),
    )

    deportista = models.ForeignKey(Deportista)
    tipo_documento_anterior = models.CharField(max_length=10, choices=TIPO_IDENTIDAD, default='CC',verbose_name='Tipo de documento actual', help_text='Este es el tipo de documento que tiene el deportista actualmente')
    identificacion_anterior = models.CharField(max_length=100,verbose_name='Identificación actual',help_text='Este es el número de documento actual o valor de documento en caso diferente a CC y TI')
    tipo_documento_nuevo = models.CharField(max_length=10, choices=TIPO_IDENTIDAD, default='CC',verbose_name='Nuevo tipo de documento', help_text='Este es el tipo de documento que tendrá una vez de click en cambiar')
    identificacion_nuevo = models.CharField(max_length=100,verbose_name='Nueva identificación', help_text='Este es el número o valor de documento que tendrá una vez de click en cambiar')


class InformacionAdicional(models.Model):
    deportista = models.ForeignKey(Deportista)
    usa_centros_biomedicos = models.BooleanField(verbose_name='¿Usa centros biomédicos?')
    es_beneficiario_programa_apoyo = models.BooleanField(verbose_name='¿Es beneficiario de algún programa de apoyo?')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

class HistorialLesiones(models.Model):
    TIPOS_LESION = (
        (5,'ESGUINCE'),
        (1,'FRACTURA'),
        (4,'LESIÓN MENISCAL'),
        (2,'LUXACIÓN'),
        (3,'RUPTURA'),
    )
    PERIODOS_REHABILITACION = (
        (1,'MENOR A 1 MES'),
        (2,'ENTRE 1 y 3 MESES'),
        (3,'ENTRE 3 y 6 MESES'),
        (4,'MAYOR A 6 MESES'),
    )
    SEGMENTOS = (
        (3,'CABEZA'),
        (4,'CUELLO'),
        (2,'EXTREMIDADES INFERIORES'),
        (1,'EXTREMIDADES SUPERIORES'),
        (5,'PELVIS'),
    )
    deportista = models.ForeignKey(Deportista)
    fecha_lesion = models.DateField(verbose_name='Fecha de la lesión')
    tipo_lesion = models.IntegerField(choices=TIPOS_LESION,verbose_name='Tipo de lesión')
    periodo_rehabilitacion = models.IntegerField(choices=PERIODOS_REHABILITACION,verbose_name='Periodo de rehabilitación')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    segmento_corporal = models.IntegerField(verbose_name='Segmento Corporal', choices=SEGMENTOS,blank=True,null=True)

class HistorialDoping(models.Model):
    TIPO_IDENTIDAD = (
        ('TI', 'TARJETA DE IDENTIDAD'),
        ('CC', 'CÉDULA DE CIUDADANÍA'),
        ('CE', 'CÉDULA DE EXTRANJERÍA'),
        ('PS', 'PASAPORTE'),
    )
    deportista = models.ForeignKey(Deportista)
    nombre_delegado = models.CharField(max_length=100,verbose_name='Nombre del delegado')
    tipo_identidad_delegado = models.CharField(max_length=2,choices=TIPO_IDENTIDAD,verbose_name='Tipo de identificación del delegado')
    identificacion_delegado = models.CharField(max_length=30,verbose_name='Número de identificación del delegado')
    evento = models.CharField(max_length=300,verbose_name='Evento en el que se detectó el doping')
    fecha = models.DateField(verbose_name='Fecha en la que se detectó el doping')
    observaciones = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
