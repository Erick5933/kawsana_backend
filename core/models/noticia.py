from django.db import models
from .usuario import Usuario

class Noticia(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    imagen_url = models.URLField(blank=True)
    actualizados_en = models.DateField(auto_now=True)
    autor = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name="noticias")

    def __str__(self):
        return self.titulo or "Noticia sin título"



