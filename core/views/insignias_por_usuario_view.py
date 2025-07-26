# core/views/insignias_por_usuario_view.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.models import UsuarioInsignia, Usuario
from core.serializers.usuario_insignia_serializer import UsuarioInsigniaSerializer

class InsigniasPorUsuarioView(APIView):
    def get(self, request, usuario_id):
        try:
            usuario = Usuario.objects.get(pk=usuario_id)
        except Usuario.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        insignias = UsuarioInsignia.objects.filter(usuario=usuario)
        serializer = UsuarioInsigniaSerializer(insignias, many=True)
        return Response(serializer.data)
