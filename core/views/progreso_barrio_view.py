from rest_framework import viewsets
from core.models import ProgresoBarrio
from core.serializers.progreso_barrio_serializer import ProgresoBarrioSerializer

class ProgresoBarrioViewSet(viewsets.ModelViewSet):
    queryset = ProgresoBarrio.objects.all()
    serializer_class = ProgresoBarrioSerializer
