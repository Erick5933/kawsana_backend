from rest_framework import viewsets
from core.models import Actividad
from core.serializers.actividad_serializer import ActividadSerializer

class ActividadViewSet(viewsets.ModelViewSet):
    queryset = Actividad.objects.all()
    serializer_class = ActividadSerializer
