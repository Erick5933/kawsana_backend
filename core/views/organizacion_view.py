from rest_framework import viewsets
from core.models import Organizacion
from core.serializers.organizacion_serializer import OrganizacionSerializer

class OrganizacionViewSet(viewsets.ModelViewSet):
    queryset = Organizacion.objects.all()
    serializer_class = OrganizacionSerializer
