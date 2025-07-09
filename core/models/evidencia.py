from django.db import models
from django.utils import timezone
from ..models.usuario import Usuario
from .actividad import Actividad

class EvidenciaActividad(models.Model):
    TIPO_ARCHIVO_CHOICES = [
        ("imagen", "Imagen"),
        ("video", "Video"),
        ("otro", "Otro"),
    ]
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="evidencias")
    archivo_url = models.URLField()
    tipo_archivo = models.CharField(max_length=10, choices=TIPO_ARCHIVO_CHOICES)
    descripcion = models.TextField(blank=True)
    fecha_subida = models.DateField(default=timezone.now)
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE, related_name="evidencias")
    es_valida = models.BooleanField(default=False)
    validador = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name="evidencias_validadas")
    fecha_validacion = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Evidencia {self.tipo_archivo} por {self.usuario} en {self.actividad}"
