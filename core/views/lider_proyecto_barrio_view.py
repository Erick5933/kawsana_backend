from rest_framework import viewsets
from core.models import LiderProyectoBarrio
from core.serializers import LiderProyectoBarrioSerializer

class LiderProyectoBarrioViewSet(viewsets.ModelViewSet):
    queryset = LiderProyectoBarrio.objects.all()
    serializer_class = LiderProyectoBarrioSerializer
