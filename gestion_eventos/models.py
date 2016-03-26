from django.db import models
from entidades.models import Ciudad


# Create your models here.
class Participante(models.Model):
    TIPO_IDENTIDAD = (
        ('CC', 'CÉDULA DE CIUDADANÍA'),
        ('TI', 'TARJETA DE IDENTIDAD'),
        ('CE', 'CÉDULA DE EXTRANJERÍA'),
        ('PS', 'PASAPORTE'),
    )
    ESTADO = (
        (0, 'Cancelado'),
        (1, 'Preinscrito'),
        (2, 'Pendiente'),
        (3, 'Aceptado'),
        (4, 'Rechazado'),
    )

    evento_participe = models.IntegerField()
    tipo_id = models.CharField(max_length=10, choices=TIPO_IDENTIDAD, default='CC',
                               verbose_name='Tipo de Identificación')
    identificacion = models.CharField(max_length=100, verbose_name='Identificación')
    nombre = models.CharField(max_length=155, verbose_name="Nombres")
    apellido = models.CharField(max_length=155, verbose_name="Apellidos")
    fecha_nacimiento = models.DateField(verbose_name='Fecha de nacimiento')
    email = models.EmailField(verbose_name="Correo electronico")
    token_email = models.CharField(max_length=255, null=True)
    pago_registrado = models.BooleanField(default=False)
    estado = models.IntegerField(choices=ESTADO, default=1)

    class Meta:
        unique_together = ('evento_participe', 'identificacion')

    def __str__(self):
        return str(self.nombre) + " " + str(self.apellido)


class Resultado(models.Model):

    PUESTOS = (
        (1, 'PRIMER LUGAR'),
        (2, 'HASTA SEGUNDO LUGAR'),
        (3, 'HASTA TERCER LUGAR'),
    )
    actividad_perteneciente = models.IntegerField()
    titulo_competencia = models.CharField(max_length=255, verbose_name="Título alternativo (opcional)",
                                          help_text="En caso de que el título de la competencia sea diferente " +
                                                    "al de la actividad, se puede escribir aquí", null=True, blank=True)
    estado = models.IntegerField(default=1)
    cantidad_puestos = models.PositiveIntegerField(choices=PUESTOS, help_text="Cantidad de ")
    primer_lugar = models.ForeignKey(Participante)
    segundo_lugar = models.ForeignKey(Participante, null=True, blank=True, related_name="segundo_lugar_resultado")
    tercer_lugar = models.ForeignKey(Participante, null=True, blank=True, related_name="tercer_lugar_resultado")

    class Meta:
        unique_together = ('actividad_perteneciente', 'id')


class Actividad(models.Model):

    titulo = models.CharField(max_length=255, verbose_name="Título de la actividad")
    descripcion = models.TextField(verbose_name="Descripción de la actividad")
    dia_actividad = models.DateField(verbose_name="Día de la actividad")
    hora_inicio = models.TimeField(verbose_name="Hora de inicio")
    hora_fin = models.TimeField(verbose_name="Hora de finalización")
    evento_perteneciente = models.IntegerField()
    estado = models.IntegerField(default=1)
    resultado = models.ManyToManyField(Resultado)

    class Meta:
        unique_together = ('evento_perteneciente', 'id')


class Evento(models.Model):
    CATEGORIA = (
        (1, 'CAPACITACIÓN'),
        (2, 'EDUCATIVO'),
        (3, 'DEPORTIVO'),
        (4, 'CULTURAL'),
        (5, 'RECREATIVO'),
    )

    titulo_evento = models.CharField(max_length=255, verbose_name="Título del evento")
    categoria = models.IntegerField(choices=CATEGORIA, verbose_name="Categoría del evento")
    ciudad_evento = models.ForeignKey(Ciudad)
    nombre_lugar = models.CharField(max_length=255, help_text="Nombre del lugar donde se realizará el evento",
                                    verbose_name="Lugar del evento")
    direccion = models.CharField(max_length=255, help_text="Dirección del lugar del evento (georeferenciado)")
    latitud = models.FloatField()
    longitud = models.FloatField()
    fecha_inicio = models.DateField(verbose_name="Fecha de inicio del evento")
    fecha_finalizacion = models.DateField(verbose_name="Fecha de finalización del evento")
    fecha_inicio_preinscripcion = models.DateField(verbose_name="Fecha de inicio de las preinscripciones")
    fecha_finalizacion_preinscripcion = models.DateField(verbose_name="Fecha de finalización de las preinscripciones")
    imagen = models.ImageField(upload_to="fotos_eventos/", blank=True, null=True)
    video = models.CharField(max_length=255, verbose_name="Vídeo del evento (opcional)",
                             help_text="Debe ingresar un url válida de un video de youtube", blank=True, null=True)
    descripcion_evento = models.TextField(verbose_name="Descripción del evento (se usará como cuerpo de noticia)")
    costo_entrada = models.PositiveIntegerField(verbose_name="Costo de la entrada (opcional)", blank=True, null=True)
    cupo_participantes = models.PositiveIntegerField(verbose_name="Cupo para participantes")
    cupo_disponible = models.PositiveIntegerField()
    cupo_candidatos = models.IntegerField()
    participantes = models.ManyToManyField(Participante)
    actividades = models.ManyToManyField(Actividad)
    autor = models.CharField(verbose_name="Autor de la noticia", max_length=150,
                             help_text="Se usará como autor para la noticia del evento que se creará")
    estado = models.IntegerField(default=1)

    class Meta:
        permissions = (
                ("view_evento", "Permite ver eventos"),
            )
