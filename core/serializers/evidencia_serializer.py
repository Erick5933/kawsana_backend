from rest_framework import serializers
from core.models import EvidenciaActividad, Usuario, Actividad

class EvidenciaActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvidenciaActividad
        fields = '__all__'

    def update(self, instance, validated_data):
        estado_anterior = instance.estado
        instance = super().update(instance, validated_data)

        if validated_data.get("estado") == "aprobado" and estado_anterior != "aprobado":
            # Asignar puntos al usuario
            puntos = instance.actividad.puntos
            instance.usuario.puntos += puntos
            instance.usuario.save()

            # Marcar progreso del proyecto
            self.actualizar_progreso(instance.actividad.proyecto)

        return instance

    def actualizar_progreso(self, proyecto):
        actividades = proyecto.actividades.all()
        total = actividades.count()
        completadas = 0

        for actividad in actividades:
            if actividad.evidencias.filter(estado='aprobado').exists():
                completadas += 1

        if total > 0:
            porcentaje = (completadas / total) * 100
            # Guarda el progreso en el modelo del proyecto
            if porcentaje >= 100:
                proyecto.progreso = 'terminado'
            elif porcentaje > 0:
                proyecto.progreso = 'en_proceso'
            else:
                proyecto.progreso = 'por_iniciar'
            proyecto.save()
