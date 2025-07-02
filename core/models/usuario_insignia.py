from django.db import models
from django.utils import timezone
from .usuario import Usuario
from .insignia import Insignia

class UsuarioInsignia(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="insignias")
    insignia = models.ForeignKey(Insignia, on_delete=models.CASCADE, related_name="usuarios")
    fecha_obtenida = models.DateField(default=timezone.now)

    class Meta:
        unique_together = ("usuario", "insignia")

    def __str__(self):
        usuario_str = str(self.usuario) if self.usuario else "Usuario desconocido"
        insignia_str = self.insignia.nombre if self.insignia else "Insignia desconocida"
        return f"{usuario_str} obtuvo {insignia_str} el {self.fecha_obtenida}"
