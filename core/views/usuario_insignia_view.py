from rest_framework import viewsets
from core.models import UsuarioInsignia
from core.serializers.usuario_insignia_serializer import UsuarioInsigniaSerializer

class UsuarioInsigniaViewSet(viewsets.ModelViewSet):
    queryset = UsuarioInsignia.objects.all()
    serializer_class = UsuarioInsigniaSerializer
