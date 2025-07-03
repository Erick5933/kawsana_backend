from rest_framework import viewsets
from core.models import Proyecto
from core.serializers.proyecto_serializer import ProyectoSerializer

class ProyectoViewSet(viewsets.ModelViewSet):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer
