from django.db import models
from .usuario import Usuario
from .proyecto import Proyecto

class UsuarioProyecto(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="proyectos_inscritos")
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name="usuarios_inscritos")
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'proyecto')

    def __str__(self):
        return f"{self.usuario} inscrito a {self.proyecto}"
