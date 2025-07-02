from django.db import models

class Organizacion(models.Model):
    nombre = models.CharField(max_length=150)
    email_contacto = models.EmailField()
    telefono_contacto = models.CharField(max_length=15, blank=True)
    direccion = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.nombre or "Organización sin nombre"
