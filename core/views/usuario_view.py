from rest_framework import viewsets
from core.models import Usuario
from core.serializers.usuario_serializer import UsuarioSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
