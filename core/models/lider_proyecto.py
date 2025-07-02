from django.db import models
from .proyecto import Proyecto
from ..models.usuario import Usuario

class LiderProyecto(models.Model):
    lider = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="liderazgos")
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name="lideres")

    class Meta:
        unique_together = ("lider", "proyecto")

    def __str__(self):
        lider_nombre = str(self.lider) if self.lider else "Sin líder"
        proyecto_nombre = self.proyecto.nombre if self.proyecto else "Sin proyecto"
        return f"Líder {lider_nombre} en proyecto {proyecto_nombre}"
