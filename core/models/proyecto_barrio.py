from django.db import models
from .proyecto import Proyecto
from ..models.barrio import Barrio

class ProyectoBarrio(models.Model):
    barrio = models.ForeignKey(Barrio, on_delete=models.CASCADE, related_name="proyectos_asociados")
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name="barrios_asociados")

    class Meta:
        unique_together = ("barrio", "proyecto")

    def __str__(self):
        barrio_nombre = self.barrio.nombre if self.barrio else "Sin barrio"
        proyecto_nombre = self.proyecto.nombre if self.proyecto else "Sin proyecto"
        return f"{barrio_nombre} en proyecto {proyecto_nombre}"
