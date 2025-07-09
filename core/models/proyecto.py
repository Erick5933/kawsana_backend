from django.db import models
from .organizacion import Organizacion

# Proyecto con nuevo campo 'progreso'
class Proyecto(models.Model):
    ESTADO_PROGRESO_CHOICES = [
        ("por_iniciar", "Por iniciar"),
        ("en_proceso", "En proceso"),
        ("terminado", "Terminado"),
    ]

    nombre = models.CharField(max_length=150)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    descripcion = models.TextField(blank=True)
    organizacion = models.ForeignKey('Organizacion', on_delete=models.CASCADE, related_name="proyectos")
    estado = models.BooleanField(default=True)
    progreso = models.CharField(max_length=20, choices=ESTADO_PROGRESO_CHOICES, default="por_iniciar")

    def __str__(self):
        return self.nombre or "Proyecto sin nombre"

