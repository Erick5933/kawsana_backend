# api/admin.py
from django.contrib import admin
from .models import (
    Organizacion, Proyecto, Actividad, EvidenciaActividad,
    ProgresoBarrio, lider_proyecto_barrio, Barrio, Usuario, ReconocimientoResiduo, Noticia, Insignia, UsuarioInsignia 
)

admin.site.register(Organizacion)
admin.site.register(Actividad)
admin.site.register(ProgresoBarrio)
admin.site.register(EvidenciaActividad)
admin.site.register(Barrio)
admin.site.register(Usuario)
admin.site.register(ReconocimientoResiduo)
admin.site.register(Noticia)
admin.site.register(Insignia)
admin.site.register(UsuarioInsignia)