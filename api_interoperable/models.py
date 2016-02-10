from django.db import models
from snd.models import Deportista
from rest_framework import serializers

# Create your models here.
class DeportistaSerializable(serializers.ModelSerializer):
    class Meta:
        model = Deportista