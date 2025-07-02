from django.db import models
from .organizacion import Organizacion

class Proyecto(models.Model):
    nombre = models.CharField(max_length=150)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    descripcion = models.TextField(blank=True)
    organizacion = models.ForeignKey(Organizacion, on_delete=models.CASCADE, related_name="proyectos")
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre or "Proyecto sin nombre"
