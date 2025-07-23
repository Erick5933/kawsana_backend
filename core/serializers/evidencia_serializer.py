from rest_framework import serializers
from core.models import EvidenciaActividad
from django.utils import timezone

class EvidenciaActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvidenciaActividad
        fields = '__all__'

    def update(self, instance, validated_data):
        estado_anterior = instance.estado
        instance = super().update(instance, validated_data)

        if validated_data.get("estado") == "aprobado" and estado_anterior != "aprobado":
            puntos = instance.actividad.puntos
            usuario = instance.usuario
            usuario.puntos += puntos
            usuario.save()

            # Actualizar progreso del proyecto
            self.actualizar_progreso(instance.actividad)

            # Actualizar progreso del barrio
            self.actualizar_progreso_barrio(instance.actividad.proyecto, usuario.barrio)

        return instance

    def actualizar_progreso(self, actividad):
        proyecto = actividad.proyecto
        total = proyecto.actividades.count()
        completadas = proyecto.actividades.filter(evidencias__estado='aprobado').distinct().count()

        if total > 0:
            porcentaje = (completadas / total) * 100

            if porcentaje >= 100:
                proyecto.progreso = 'terminado'
            elif porcentaje > 0:
                proyecto.progreso = 'en_proceso'
            else:
                proyecto.progreso = 'por_iniciar'

            proyecto.save()

    def actualizar_progreso_barrio(self, proyecto, barrio):
        from core.models import ProgresoBarrio  # evitar import circular
        total = proyecto.actividades.count()
        completadas = proyecto.actividades.filter(evidencias__estado='aprobado', evidencias__usuario__barrio=barrio).distinct().count()

        if total > 0:
            porcentaje = (completadas / total) * 100

            progreso_barrio, _ = ProgresoBarrio.objects.get_or_create(
                proyecto=proyecto,
                barrio=barrio,
                defaults={'progreso': 0.0}
            )
            progreso_barrio.progreso = porcentaje
            progreso_barrio.ultima_actualizacion = timezone.now().date()
            progreso_barrio.save()
