from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from .proyecto import Proyecto
from ..models.barrio import Barrio

class ProgresoBarrio(models.Model):
    ultima_actualizacion = models.DateField(default=timezone.now)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name="progresos")
    progreso = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)], default=0.0)
    barrio = models.ForeignKey(Barrio, on_delete=models.CASCADE, related_name="progresos")

    class Meta:
        unique_together = ("proyecto", "barrio")

    def __str__(self):
        return f"Progreso {self.progreso}% en {self.barrio} para {self.proyecto}"
