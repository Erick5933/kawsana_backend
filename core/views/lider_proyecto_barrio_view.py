from rest_framework import viewsets, status
from rest_framework.response import Response
from core.models import LiderProyectoBarrio, UsuarioProyecto, Usuario
from core.serializers.lider_proyecto_barrio_serializer import LiderProyectoBarrioSerializer

from rest_framework.response import Response
from rest_framework import status

class LiderProyectoBarrioViewSet(viewsets.ModelViewSet):
    queryset = LiderProyectoBarrio.objects.all()
    serializer_class = LiderProyectoBarrioSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print("Errores serializer LiderProyectoBarrio:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

