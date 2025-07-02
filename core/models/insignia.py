from django.db import models

class Insignia(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    icono_url = models.URLField(blank=True)

    def __str__(self):
        return self.nombre or "Insignia sin nombre"
