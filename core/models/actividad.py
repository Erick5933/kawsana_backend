from django.db import models
from django.core.validators import MinValueValidator
from .proyecto import Proyecto

class Actividad(models.Model):
    nombre = models.CharField(max_length=150)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    descripcion = models.TextField(blank=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name="actividades")
    estado = models.BooleanField(default=True)
    puntos = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        proyecto_nombre = self.proyecto.nombre if self.proyecto else "Sin proyecto"
        return f"{self.nombre} ({proyecto_nombre})"
