#encoding:utf-8

from entidades.models import *
from django.db import models


class Dirigente(models.Model):
    nombre = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    superior = models.ForeignKey('Dirigente', null=True, blank=True); # las comillas fuerza un lazy reference, necesario por la referencia cíclica
    foto = models.ImageField(upload_to='fotos', null=True, blank=True)
    entidad = models.ForeignKey(Entidad, null=True, blank=True)

    def __str__(self):
        return self.nombre