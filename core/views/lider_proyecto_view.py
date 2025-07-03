from rest_framework import viewsets
from core.models import LiderProyecto
from core.serializers.lider_proyecto_serializer import LiderProyectoSerializer

class LiderProyectoViewSet(viewsets.ModelViewSet):
    queryset = LiderProyecto.objects.all()
    serializer_class = LiderProyectoSerializer
