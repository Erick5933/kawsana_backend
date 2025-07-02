from django.db import models

class Barrio(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    ciudad = models.CharField(max_length=100, default="Cuenca")
    num_habitantes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.nombre} ({self.ciudad})"
