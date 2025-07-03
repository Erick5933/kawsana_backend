from rest_framework import viewsets
from core.models import Barrio
from core.serializers.barrio_serializer import BarrioSerializer

class BarrioViewSet(viewsets.ModelViewSet):
    queryset = Barrio.objects.all()
    serializer_class = BarrioSerializer
