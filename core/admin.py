# api/admin.py
from django.contrib import admin
from .models import (
    Organizacion, Proyecto, Actividad, EvidenciaActividad,
    ProgresoBarrio, ProyectoBarrio, LiderProyecto
)

admin.site.register(Organizacion)
admin.site.register(Proyecto)
admin.site.register(Actividad)
admin.site.register(EvidenciaActividad)
admin.site.register(ProgresoBarrio)
admin.site.register(ProyectoBarrio)
admin.site.register(LiderProyecto)
