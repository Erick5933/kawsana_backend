from rest_framework import viewsets
from core.models import ProyectoBarrio
from core.serializers.proyecto_barrio_serializer import ProyectoBarrioSerializer

class ProyectoBarrioViewSet(viewsets.ModelViewSet):
    queryset = ProyectoBarrio.objects.all()
    serializer_class = ProyectoBarrioSerializer
