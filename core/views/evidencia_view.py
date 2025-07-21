from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from core.models import EvidenciaActividad
from core.serializers.evidencia_serializer import EvidenciaActividadSerializer
from datetime import timezone

class EvidenciaActividadViewSet(viewsets.ModelViewSet):
    queryset = EvidenciaActividad.objects.all()
    serializer_class = EvidenciaActividadSerializer

    @action(detail=True, methods=['post'], url_path='validar')
    def validar_evidencia(self, request, pk=None):
        evidencia = self.get_object()
        estado = request.data.get("estado")  # "aprobado" o "rechazado"

        if estado not in ["aprobado", "rechazado"]:
            return Response({"error": "Estado inválido"}, status=status.HTTP_400_BAD_REQUEST)

        evidencia.estado = estado
        evidencia.validador = request.user
        evidencia.fecha_validacion = timezone.now()
        evidencia.save()

        serializer = self.get_serializer(evidencia)
        return Response(serializer.data)
