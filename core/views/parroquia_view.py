from rest_framework import viewsets
from core.models import Parroquia
from core.serializers.parroquia_serializer import ParroquiaSerializer

class ParroquiaViewSet(viewsets.ModelViewSet):
    queryset = Parroquia.objects.all()
    serializer_class = ParroquiaSerializer
