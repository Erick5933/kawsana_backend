from django.db import models
from django.utils import timezone
from ..models.usuario import Usuario
from .actividad import Actividad

def evidencia_upload_path(instance, filename):
    return f'evidencias/{instance.usuario.id}/{filename}'

class EvidenciaActividad(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="evidencias")
    archivo = models.FileField(upload_to=evidencia_upload_path, null=True, blank=True)
    descripcion = models.TextField(blank=True)
    fecha_subida = models.DateField(default=timezone.now)
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE, related_name="evidencias")
    es_valida = models.BooleanField(default=False)
    validador = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name="evidencias_validadas")
    fecha_validacion = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Evidencia por {self.usuario} en {self.actividad}"
