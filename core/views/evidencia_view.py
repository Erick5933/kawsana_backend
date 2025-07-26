from core.models import EvidenciaActividad, Usuario, ProgresoBarrio, LiderProyectoBarrio
from core.serializers.evidencia_serializer import EvidenciaActividadSerializer
from core.utils.insignias import verificar_insignias
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from core.utils.actividad import completar_actividad


class EvidenciaActividadViewSet(viewsets.ModelViewSet):
    queryset = EvidenciaActividad.objects.all()
    serializer_class = EvidenciaActividadSerializer
    permission_classes = [AllowAny]

    @action(detail=True, methods=['post'], url_path='validar')
    def validar_evidencia(self, request, pk=None):
        evidencia = self.get_object()
        estado = request.data.get("estado")  # "aprobado" o "rechazado"

        if estado not in ["aprobado", "rechazado"]:
            return Response({"error": "Estado inválido"}, status=status.HTTP_400_BAD_REQUEST)

        estado_anterior = evidencia.estado
        evidencia.estado = estado

        # Asignar validador
        if request.user.is_authenticated and hasattr(request.user, 'usuario'):
            evidencia.validador = request.user.usuario
        else:
            evidencia.validador = Usuario.objects.first()  # Puedes personalizar esto

        evidencia.fecha_validacion = timezone.now()
        evidencia.save()

        if estado == "aprobado" and estado_anterior != "aprobado":
            # Completar actividad
            completar_actividad(evidencia.actividad, evidencia.usuario)

            puntos_a_sumar = evidencia.actividad.puntos
            usuario = evidencia.usuario
            usuario.puntos += puntos_a_sumar
            usuario.save()

            # 🔁 Sumar puntos a todos los usuarios del MISMO BARRIO (excepto el que subió la evidencia)
            if usuario.barrio:
                usuarios_barrio = Usuario.objects.filter(barrio=usuario.barrio).exclude(id=usuario.id)
                for u in usuarios_barrio:
                    u.puntos += puntos_a_sumar
                    u.save()

                    # Verificar insignias también para estos usuarios
                    verificar_insignias(u)

            # Verificar insignias para quien subió la evidencia
            verificar_insignias(usuario)

        serializer = self.get_serializer(evidencia)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        evidencia = self.get_object()
        data = request.data

        estado_anterior = evidencia.estado
        nuevo_estado = data.get('estado')

        if estado_anterior != 'aprobado' and nuevo_estado == 'aprobado':
            puntos_a_sumar = evidencia.actividad.puntos

            usuario = evidencia.usuario
            usuario.puntos += puntos_a_sumar
            usuario.save()

            if usuario.barrio:
                usuarios_mismo_barrio = Usuario.objects.filter(barrio=usuario.barrio).exclude(id=usuario.id)
                for u in usuarios_mismo_barrio:
                    u.puntos += puntos_a_sumar
                    u.save()
                    verificar_insignias(u)

            verificar_insignias(usuario)

        return super().update(request, *args, **kwargs)
