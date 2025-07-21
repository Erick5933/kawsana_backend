from django.db import models
from django.utils import timezone
from .usuario import Usuario
from .insignia import Insignia

class UsuarioInsignia(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="insignias")
    insignia = models.ForeignKey(Insignia, on_delete=models.CASCADE)
    fecha_asignacion = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('usuario', 'insignia')  # Evita duplicados

    def __str__(self):
        return f"{self.usuario} - {self.insignia}"
