from django.db import models
from datetime import date
from django.utils import timezone

class Insignia(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    puntos_necesarios = models.PositiveIntegerField(default=0)
    icono = models.ImageField(upload_to='insignias/', default='insignias/insignia.png')
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nombre

