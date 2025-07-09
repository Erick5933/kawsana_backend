from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from .proyecto import Proyecto
from .barrio import Barrio

# Nuevo modelo reemplazando LiderProyecto
class LiderProyectoBarrio(models.Model):
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name="liderazgos_barrio")
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name="lideres_barrio")
    barrio = models.ForeignKey(Barrio, on_delete=models.CASCADE, related_name="lideres_proyecto")

    class Meta:
        unique_together = ("usuario", "proyecto", "barrio")

    def __str__(self):
        return f"{self.usuario} lidera {self.proyecto} en {self.barrio}"

