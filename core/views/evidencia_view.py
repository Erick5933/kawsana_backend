from rest_framework import viewsets
from core.models import EvidenciaActividad
from core.serializers.evidencia_serializer import EvidenciaActividadSerializer

class EvidenciaActividadViewSet(viewsets.ModelViewSet):
    queryset = EvidenciaActividad.objects.all()
    serializer_class = EvidenciaActividadSerializer
