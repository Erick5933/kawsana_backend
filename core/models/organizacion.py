from django.db import models
from django.core.validators import RegexValidator  # Import necesario

# Organización con ruc y representante
class Organizacion(models.Model):
    nombre = models.CharField(max_length=150)
    ruc = models.CharField(
        max_length=13,
        unique=True,
        validators=[RegexValidator(r'^\d{13}$', 'El RUC debe tener 13 dígitos')],
        default='0000000000000'  # o algún valor que uses como placeholder
    )

    representante = models.CharField(max_length=150, null=True, blank=True)
    email_contacto = models.EmailField()
    telefono_contacto = models.CharField(max_length=15, blank=True)
    direccion = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.nombre or "Organización sin nombre"
