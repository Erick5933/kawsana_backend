from django.db import models
from core.models.ciudad import Ciudad  # Asegúrate de que este archivo también esté bien

class Parroquia(models.Model):
    nombre = models.CharField(max_length=100)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE, related_name="parroquias")

    class Meta:
        unique_together = ("nombre", "ciudad")

    def __str__(self):
        return f"{self.nombre} ({self.ciudad.nombre})"
