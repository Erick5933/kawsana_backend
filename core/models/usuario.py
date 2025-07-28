from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from .barrio import Barrio
from django.utils.timezone import localdate

class Usuario(models.Model):
    TIPO_USUARIO_CHOICES = [
        ("ciudadano", "Ciudadano"),
        ("lider", "Líder"),
        ("organizacion", "Organización"),
    ]

    usuario = models.CharField(
        max_length=30,
        unique=True,
        null=True,
        blank=True,
        help_text="Nombre de usuario único"
    )

    email = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=128)
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO_CHOICES)
    barrio = models.ForeignKey(Barrio, on_delete=models.SET_NULL, null=True, blank=True, related_name="usuarios")
    fecha_registro = models.DateField(default=localdate)
    estado = models.BooleanField(default=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    cedula = models.CharField(
        max_length=10,
        unique=True,
        validators=[RegexValidator(r'^\d{10}$', 'Cédula debe tener 10 dígitos numéricos')]
    )
    telefono = models.CharField(
        max_length=15,
        blank=True,
        validators=[RegexValidator(r'^\+?\d{7,15}$', 'Número de teléfono inválido')]
    )
    direccion = models.CharField(max_length=255, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    puntos = models.PositiveIntegerField(default=0)  # <- Agrega este campo

    def __str__(self):
        return f"{self.usuario} - {self.nombres} {self.apellidos} ({self.email})"
