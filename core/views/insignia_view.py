from rest_framework import viewsets
from core.models import Insignia
from core.serializers.insignia_serializer import InsigniaSerializer

class InsigniaViewSet(viewsets.ModelViewSet):
    queryset = Insignia.objects.all()
    serializer_class = InsigniaSerializer
