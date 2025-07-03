from rest_framework import viewsets
from core.models import ReconocimientoResiduo
from core.serializers.reconocimiento_serializer import ReconocimientoResiduoSerializer

class ReconocimientoResiduoViewSet(viewsets.ModelViewSet):
    queryset = ReconocimientoResiduo.objects.all()
    serializer_class = ReconocimientoResiduoSerializer
