from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from core.models import EvidenciaActividad
from core.serializers.evidencia_serializer import EvidenciaActividadSerializer
from django.utils import timezone
from rest_framework.permissions import AllowAny

class EvidenciaActividadViewSet(viewsets.ModelViewSet):
    queryset = EvidenciaActividad.objects.all()
    serializer_class = EvidenciaActividadSerializer
    permission_classes = [AllowAny]  # permite sin token

    @action(detail=True, methods=['post'], url_path='validar')
    def validar_evidencia(self, request, pk=None):
        evidencia = self.get_object()
        estado = request.data.get("estado")  # "aprobado" o "rechazado"

        if estado not in ["aprobado", "rechazado"]:
            return Response({"error": "Estado inválido"}, status=status.HTTP_400_BAD_REQUEST)

        evidencia.estado = estado

        # Asignar un validador genérico para pruebas, si no hay usuario autenticado
        if request.user.is_authenticated and hasattr(request.user, 'usuario'):
            evidencia.validador = request.user.usuario  # si usas CustomUser y hay relación
        else:
            from core.models import Usuario
            evidencia.validador = Usuario.objects.first()  # usuario cualquiera para pruebas (mejor uno creado para esto)

        evidencia.fecha_validacion = timezone.now()
        evidencia.save()

        serializer = self.get_serializer(evidencia)
        return Response(serializer.data)