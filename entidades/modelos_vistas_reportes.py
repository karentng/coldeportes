from django.db import models
from entidades.models import *
from snd.models import *

class PublicEscenarioView(models.Model):
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

class PublicEscenarioEstratoView(models.Model):
    
    class Meta:
        managed = False
            
    id_escenario = models.ForeignKey(Escenario)
    ciudad = models.ForeignKey(Ciudad)
    fecha_creacion = models.DateTimeField()    
    estrato = models.CharField(max_length=1)
    tipodisciplinadeportiva = models.ForeignKey(TipoDisciplinaDeportiva)
    cantidad = models.PositiveIntegerField()
    estado = models.IntegerField(choices=Escenario.ESTADOS, verbose_name="estado del Escenario")
    
    
    
class PublicCafView(models.Model):
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

class PublicPersonalApoyoView(models.Model):
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

class PublicDeportistaView(models.Model):
    class Meta:
        managed = False

    TIPOS_LESION = {
        1:'FRACTURA',
        2:'LUXACIÓN',
        3:'RUPTURA',
        4:'LESIÓN MENISCAL',
        5:'ESGUINCE',
    }

    PERIODOS_REHABILITACION = {
        1:'MENOR A 1 MES',
        2:'ENTRE 1 y 3 MESES',
        3:'ENTRE 3 y 6 MESES',
        4:'MAYOR A 6 MESES',
    }

    class Meta:
        managed = False

    #campos modelo deportista
    genero = models.CharField(max_length=11)
    ciudad_residencia = models.ForeignKey(Ciudad)
    disciplinas = models.ForeignKey(TipoDisciplinaDeportiva)
    fecha_nacimiento = models.DateField()
    fecha_creacion = models.DateTimeField()
    lgtbi = models.BooleanField()
    etnia = models.CharField(max_length=20)
    nacionalidad = models.ForeignKey(Nacionalidad)
    estado = models.IntegerField()

    #campos historial deportivo
    tipo_participacion = models.CharField(max_length=100)
    estado_participacion = models.CharField(max_length=50)

    #campos informacion academica
    nivel_formacion = models.CharField(max_length=20)
    estado_formacion = models.CharField(max_length=20)

    #campos informacion adicional
    usa_centros_biomedicos = models.BooleanField()
    es_beneficiario_programa_apoyo = models.BooleanField()

    #campos historial lesiones
    tipo_lesion = models.IntegerField()
    periodo_rehabilitacion = models.IntegerField()

    #campos doping
    fecha_doping = models.DateField()

    def return_display_lesion(self,dic,is_tipo):
        ids = [id for id in dic]
        dic_nombres = self.TIPOS_LESION if is_tipo else self.PERIODOS_REHABILITACION
        for elemento in ids:
            if None == elemento:
                dic['NINGUNA LESIÓN'] = dic[None]
                del dic[None]
            else:
                dic[dic_nombres[elemento]] = dic[elemento]
                del dic[elemento]
        return dic
