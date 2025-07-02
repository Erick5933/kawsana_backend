from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from .usuario import Usuario

class ReconocimientoResiduo(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="residuos_reconocidos")
    fecha = models.DateField(default=timezone.now)
    tipo_residuo = models.CharField(max_length=100)
    porcentaje_confianza = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    imagen = models.URLField()

    def __str__(self):
        return f"{self.tipo_residuo} reconocido por {self.usuario} con {self.porcentaje_confianza}%"
