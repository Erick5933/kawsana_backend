from rest_framework import viewsets
from core.models import Noticia
from core.serializers.noticia_serializer import NoticiaSerializer

class NoticiaViewSet(viewsets.ModelViewSet):
    queryset = Noticia.objects.all()
    serializer_class = NoticiaSerializer
