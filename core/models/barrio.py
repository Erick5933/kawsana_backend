from django.db import models
from .parroquia import Parroquia

class Barrio(models.Model):
    nombre = models.CharField(max_length=100)
    parroquia = models.ForeignKey(Parroquia, on_delete=models.CASCADE, related_name="barrios", null=True, blank=True)
    num_habitantes = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("nombre", "parroquia")

    def __str__(self):
        return f"{self.nombre} ({self.parroquia.nombre if self.parroquia else 'Sin parroquia'})"

